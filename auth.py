import click
import firebase_admin
from firebase_admin import auth, credentials, firestore


@click.group()
def cli():
    """Authorize user email to access write to firestore and cloud storage

    Please delete credentials.json after using it\n
    For next time re-generate it
    """
    try:
        cred = credentials.Certificate("./credentials.json")
        firebase_admin.initialize_app(cred)
    except FileNotFoundError:
        click.echo(
            "please add service account credentials in this folder by the name credentials.json"
        )
        raise SystemExit(1)

    pass


@cli.command(help="Add and Authorize email")
@click.argument(
    "email",
    type=click.STRING,
)
def authorize(email):
    db = firestore.client()

    try:
        user = auth.get_user_by_email(email)
    except auth._auth_utils.UserNotFoundError:
        click.echo(
            "User didn't signed in the app. Request the user to sign-in in the app with google"
        )
        raise SystemExit(1)

    custom_claims = {"writer": True}

    try:
        auth.set_custom_user_claims(user.uid, custom_claims)
        click.echo("Custom claims set successfully")
    except Exception as e:
        click.echo(f"Error setting custom claims: {e}")
        raise SystemExit(1)

    authorize = {"authorized": True}

    try:
        db.collection("roles").document(email).set(authorize)
        click.echo("Added authorization in roles collection")
    except Exception as e:
        click.echo(f"Error setting document in roles collection: {e}")
        raise SystemExit(1)

    click.echo("Successful in authorizing user")
    return


@cli.command(help="Check if email is authorized or not")
@click.argument(
    "email",
    type=click.STRING,
)
def check(email):
    toAdd = 0
    db = firestore.client()

    try:
        user = auth.get_user_by_email(email)
    except auth._auth_utils.UserNotFoundError:
        click.echo("User didn't signed in the app")
        raise SystemExit(1)
    except Exception as e:
        click.echo(f"Err while checking if user exists or not: {e}")
        raise SystemExit(1)

    if user.custom_claims == None:
        click.echo("Writer role is not assigned to user account")
        toAdd += 1
    elif user.custom_claims.get("writer") == True:
        click.echo("Writer role is assigned to user account")

    roles_ref = db.collection("roles").document(email)

    try:
        doc = roles_ref.get()
    except Exception as e:
        click.echo(f"Error getting document from roles collection: {e}")
        raise SystemExit(1)

    if doc.exists:
        isAuthorized = doc.to_dict()["authorized"]
        if isAuthorized == True:
            click.echo(
                "User exists in roles collection and it's value is set to authorized"
            )
        elif isAuthorized == False:
            click.echo(
                "User exists in roles collection but it's value is not set to authorized"
            )
            toAdd += 1
    else:
        click.echo("User is not added in roles collection")
        toAdd += 1

    if toAdd > 0:
        click.echo("To resolve all above and authorize user, use authorize subcommand")

    return


@cli.command(help="Delete user account and revoked authorization")
@click.argument(
    "email",
    type=click.STRING,
)
def delete(email):
    db = firestore.client()

    try:
        user = auth.get_user_by_email(email)
    except auth._auth_utils.UserNotFoundError:
        click.echo("User didn't signed in the app")
        raise SystemExit(1)
    except Exception as e:
        click.echo(f"Err while checking if user exists or not: {e}")
        raise SystemExit(1)

    try:
        auth.delete_user(user.uid)
    except Exception as e:
        click.echo(f"Err while deleting user: {e}")
        raise SystemExit(1)

    try:
        db.collection("roles").document(email).delete()
    except Exception as e:
        click.echo(f"Err when delete document from roles collection: {e}")
        raise SystemExit(1)

    click.echo("successfully deleted user account and revoke authorization")
    return


if __name__ == "__main__":
    cli()
