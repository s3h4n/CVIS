from flask import (
    send_from_directory,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request,
    Blueprint,
)
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.utils import secure_filename
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from packages import FormReceiver
from packages import DatabaseHelper
from packages import Token
from models import User, AuthUser
from forms import LoginForm, RegisterForm
from application import create_app, db, login_manager, bcrypt
import datetime
import constants as c
import base64
import shutil
import os
import re

blue_print = Blueprint("routes", __name__)


@login_manager.user_loader
def load_user(user_id):
    return AuthUser.query.get(int(user_id))


app = create_app()


@blue_print.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=1)


"""s
--------------------------------------------------
|                                                |
|                API END POINTS                  |
|                                                |
--------------------------------------------------
"""


@blue_print.route("/api/user-registration", methods=["POST"])
def register_user():
    form = FormReceiver()
    token = Token()
    db_helper = DatabaseHelper()

    try:
        # Get form inputs and images seperately
        new_user = User(
            user_token=token.get(
                user_id=request.form["uid"], user_dob=request.form["dob"]
            ),
            first_name=request.form["firstName"],
            last_name=request.form["lastName"],
            dob=request.form["dob"],
            gender=request.form["gender"],
            email=request.form["email"],
            mobile=request.form["mobile"],
            addr_line_1=request.form["addrLine1"],
            addr_line_2=request.form["addrLine2"],
            town=request.form["town"],
            uid=request.form["uid"],
            uid_type=request.form["uidType"],
            vac_count=int(request.form["vacCount"]),
        )
        form_images = form.get_files(c.USER_REG_FILES)

        is_transmission_success = True  # Data successfully recieved
    except Exception as e:
        is_transmission_success = e

    if is_transmission_success:
        # Display previously fetched data
        print("\n >>> Log ::: Registration form data :\n", new_user)
        print("\n >>> Log ::: Registration form images :\n", form_images)

        # Check user existance
        is_user_exists = (
            db.session.query(
                db.exists().where(
                    User.uid == new_user.uid and User.uid_type == new_user.uid_type
                )
            ).scalar()
            or db.session.query(
                db.exists().where(User.email == new_user.email)
            ).scalar()
            or db.session.query(
                db.exists().where(
                    User.user_token == new_user.user_token,
                )
            ).scalar()
        )

        try:
            is_images_exists = os.listdir(
                os.path.join(c.IMAGE_DB_PATH, new_user.user_token)
            )
        except Exception as e:
            is_images_exists = False

        # Display previously fetched data
        print("\n >>> Log ::: User info existance check results :\n", is_user_exists)
        print("\n >>> Log ::: User image existance check results :\n", is_images_exists)

        if is_user_exists == False and is_images_exists == False:
            db.session.add(new_user)
            db.session.commit()

            image_result = db_helper.save_image(
                main_dir=c.IMAGE_DB_PATH,
                user_token=new_user.user_token,
                images=form_images,
            )

            # Display previously fetched data
            print("\n >>> Log ::: Adding new data results :\n", new_user)
            print("\n >>> Log ::: Adding new images results :\n", image_result)

            if image_result == True:
                return {
                    "status": "true",
                    "message": "You have successfully registered in the system.",
                }
            elif image_result == False:
                return {
                    "status": "false",
                    "message": "There was an error while registration process. Please try again.",
                }

        return {"status": "false", "message": "User is already in the system."}

    return e


@blue_print.route("/api/request-id", methods=["POST"])
def request_id():
    form = FormReceiver()
    db_helper = DatabaseHelper()

    response = form.get_data(
        [
            "email",
            "uid",
            "uidType",
        ]
    )

    # Check user existance
    is_user_exists = db.session.query(
        db.exists().where(
            User.uid == response["uid"],
            User.uid_type == response["uidType"],
            User.email == response["email"],
        )
    ).scalar()

    # Display previously fetched data
    print("\n >>> Log ::: User check result :\n", is_user_exists)

    if is_user_exists != False:
        try:
            return (
                db.session.query(User.user_token)
                .filter(
                    User.uid == response["uid"],
                    User.uid_type == response["uidType"],
                    User.email == response["email"],
                )
                .one()
            )[0]
            # return userToken if user data is available.
        except Exception as e:
            return {
                "status": "false",
                "message": f"{e}",
            }
    else:
        return {
            "status": "false",
            "message": "We can't find your data in the system. Maybe you haven't registered yet.",
        }


@blue_print.route("/api/validate-id", methods=["POST"])
def validate_user():
    form = FormReceiver()

    response = form.get_data(["userToken"])

    try:
        user = (
            db.session.query(User.status, User.first_name, User.last_name, User.uid)
            .filter(User.user_token == response["userToken"])
            .one()
        )

        # Display previously fetched data
        print("\n >>> Log ::: User check result :\n", user)

        if user.status == 1:
            return f"{user.first_name} {user.last_name} ({user.uid}) is vaccinated."
        elif user.status == 0:
            return f"{user.first_name} {user.last_name} ({user.uid}) is not vaccinated."

    except Exception as e:
        return "We couldn't find any matching data for the QR code. Please request new one and try again."


"""
--------------------------------------------------
|                                                |
|                  USER ROUTES                   |
|                                                |
--------------------------------------------------
"""


@blue_print.route("/")
def base():
    return send_from_directory("templates/user/dist", "index.html")


@blue_print.route("/<path:path>")
def home(path):
    return send_from_directory("templates/user/dist", path)


"""
--------------------------------------------------
|                                                |
|                  ADMIN ROUTES                  |
|                                                |
--------------------------------------------------
"""


# User Authentication
@blue_print.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check if user information exists or not
        is_info_exists = db.session.query(
            db.exists().where(AuthUser.email == form.email.data)
        ).scalar()

        if is_info_exists:
            try:
                user = AuthUser.query.filter_by(email=form.email.data).first()
                if check_password_hash(user.password, form.pwd.data):
                    login_user(user)
                    return redirect(url_for("routes.dashboard"))
                else:
                    flash("Invalid Username or password!", "danger")
            except Exception as e:
                flash(e, "danger")
        else:
            flash("User doesn't exist. Please create an account first.", "danger")

    return render_template(
        "auth/auth.html", form=form, text="Login", title="Login", btn_action="Login"
    )


@blue_print.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.pwd.data
            username = form.username.data

            newuser = AuthUser(
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(password),
            )

            print(newuser)

            x = db.session.add(newuser)
            db.session.commit()

            print(newuser, x)

            flash(f"Account Succesfully created", "success")
            return redirect(url_for("routes.login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

    return render_template(
        "auth/auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account",
    )


@blue_print.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))


@blue_print.route("/admin/dashboard/")
@login_required
def dashboard():
    confirmed_users = db.session.query(User.user_token).filter(User.status == 1).all()
    unconfirmed_users = db.session.query(User.user_token).filter(User.status == 0).all()

    user_reg_date = [str(n[0])[8:10] for n in (db.session.query(User.created_at).all())]
    today = str(datetime.datetime.now())[8:10]

    all_users_count = len([n[0] for n in (db.session.query(User.user_token).all())])

    user_vac_count = [
        len(db.session.query(User.vac_count).filter(User.vac_count == 1).all()),
        len(db.session.query(User.vac_count).filter(User.vac_count == 2).all()),
        len(db.session.query(User.vac_count).filter(User.vac_count == 3).all()),
        len(db.session.query(User.vac_count).filter(User.vac_count == 4).all()),
    ]

    return render_template(
        "/admin/dashboard.html",
        confirmed_users=len(confirmed_users),
        unconfirmed_users=len(unconfirmed_users),
        today_users=len([c for c in user_reg_date if c == today]),
        all_users_count=all_users_count,
        user_vac_count=user_vac_count,
    )


@blue_print.route("/admin/dashboard/search", methods=["POST"])
@login_required
def find_user():
    form = FormReceiver()
    db_helper = DatabaseHelper()

    image_set = {}

    response = form.get_data(["uid", "uidType"])

    # Check user existance
    is_user_exists = db.session.query(
        db.exists().where(
            User.uid == response["uid"],
            User.uid_type == response["uidType"],
        )
    ).scalar()

    # Get user token if the user exists.
    token = (
        (
            db.session.query(User.user_token)
            .filter(
                User.uid == response["uid"],
                User.uid_type == response["uidType"],
            )
            .one()
        )[0]
        if is_user_exists == True
        else False
    )

    # Check if user images exists or not
    try:
        is_image_exists = (
            os.path.join(c.IMAGE_DB_PATH, token) if token != False else False
        )
    except Exception as e:
        is_image_exists = False

    # Display previously fetched data
    print("\n >>> Log ::: User check result :\n", is_user_exists)
    print("\n >>> Log ::: User image result :\n", is_image_exists)

    # Try to get images and info of given user token

    if is_user_exists == True and is_image_exists != False:
        try:
            user = (
                db.session.query(
                    User.user_token,
                    User.first_name,
                    User.last_name,
                    User.dob,
                    User.gender,
                    User.email,
                    User.mobile,
                    User.addr_line_1,
                    User.addr_line_2,
                    User.town,
                    User.uid,
                    User.uid_type,
                    User.vac_count,
                    User.status,
                    User.created_at,
                )
                .filter(User.user_token == token)
                .one()
            )

            for img in os.listdir(is_image_exists):
                img_name, img_ext = os.path.splitext(secure_filename(img))

                # Read images and encode and decode to text so HTML can directly display them
                with open(f"{os.path.join(is_image_exists)}/{img}", "rb") as image_file:
                    image_set[img_name] = (base64.b64encode(image_file.read())).decode()

            return render_template("/admin/profile.html", user=user, images=image_set)

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Getting user {token} has failed :\n", e)
            flash(f"Getting user {token} has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(
            f"Could not find the requested user. Please re-check details and try again.",
            "warning",
        )
        return redirect(request.referrer)


@blue_print.route("/admin/dashboard/cleanup-database/")
@login_required
def cleanup_database():
    # Get all rows from database
    all_user_tokens = [token for token in db.session.query(User.user_token)]

    all_user_img_dirs = os.listdir(c.IMAGE_DB_PATH)

    # Display results
    print("\n >>> Log ::: All user tokens :\n", all_user_tokens)
    print("\n >>> Log ::: All user image directories  :\n", all_user_img_dirs)

    if len(all_user_tokens) > 0:
        tokens_without_imgs = [
            t[0] for t in all_user_tokens if t[0] not in [i for i in all_user_img_dirs]
        ]

        # Display results
        print("\n >>> Log ::: Tokens that doesn't have images :\n", tokens_without_imgs)

        for token in tokens_without_imgs:
            delete_info_result = User.query.filter_by(user_token=token).delete()
            db.session.commit()
            print(f"\n >>> Log ::: Deleting {token} :\n", delete_info_result)

        if len(tokens_without_imgs) > 0:
            flash(
                f"Following users were deleted because there were no image directories for them : {tokens_without_imgs}",
                "warning",
            )

    if len(all_user_img_dirs) > 0:
        imgs_without_tokens = [
            i for i in all_user_img_dirs if i not in [t[0] for t in all_user_tokens]
        ]

        # Display results
        print("\n >>> Log ::: Images that doesn't have tokens :\n", imgs_without_tokens)

        for img_dir in imgs_without_tokens:
            print(img_dir)
            result = shutil.rmtree(os.path.join(c.IMAGE_DB_PATH, img_dir))
            print(f"\n >>> Log ::: Deleting {img_dir} :\n", result)

        if len(imgs_without_tokens) > 0:
            flash(
                f"Following image directories  were deleted because there were no user tokens for them : {imgs_without_tokens}",
                "warning",
            )

    return redirect(request.referrer)


# User Management
@blue_print.route("/admin/users/auth/all/")
@login_required
def manage_auth_users():
    try:
        # Get all rows from database
        users = AuthUser.query.all()

        # Display results
        print("\n >>> Log ::: All admin users :\n", users)

        if len(users) <= 0:
            flash(f"No users found.", "warning")
            return render_template("/admin/u_management.html", users=[])
        else:
            return render_template("/admin/u_management.html", users=users)

    except Exception as e:
        flash(f"There is an error while displaying data. {e}", "danger")
        return render_template("/admin/u_management.html", users=[])


@blue_print.route("/admin/users/auth/all/<email>=<new_role>/")
@login_required
def update_user_role(email, new_role):
    # Check if user information exists or not
    is_info_exists = db.session.query(
        db.exists().where(AuthUser.email == email)
    ).scalar()

    # Display existance check results
    print("\n >>> Log ::: User information check output :\n", is_info_exists)

    if is_info_exists == True:
        try:
            user = AuthUser.query.filter_by(email=email).first()
            user.role = new_role
            db.session.commit()

            # Display results
            print(
                "\n >>> Log ::: User role update results :\n",
                user,
            )

            user = AuthUser.query.filter_by(email=email).first()

            # Display results
            print(
                "\n >>> Log ::: New user role :\n",
                user.email,
            )

            flash(
                f"Role set to {'Admin' if user.role == 1 else 'Guest' if user.role == 0 else 'Super Admin'}",
                "info",
            )

            return redirect(request.referrer)

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Updating user role has failed :\n", e)
            flash(f"Updating user role has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(f"Updating user role has failed.", "danger")
        return redirect(request.referrer)


@blue_print.route("/admin/users/auth/all/filter/<role>")
@login_required
def filter_auth_users(role):
    try:
        # Get all rows from database where role is set to 1
        users = AuthUser.query.filter(AuthUser.role == role).all()

        # Display results
        print("\n >>> Log ::: Result :\n", users)

        if len(users) <= 0:
            flash(f"No users found.", "warning")
            return render_template("/admin/u_management.html", users=[])
        else:
            return render_template("/admin/u_management.html", users=users)

    except Exception as e:
        flash(f"There is an error while displaying data. {e}", "danger")
        return render_template("/admin/confirmed_users.html", users=[])


@blue_print.route("/admin/users/auth/all/search")
@login_required
def search_auth_users():
    try:
        search_query = str(request.args.get("searchInp"))
        search_filter = str(request.args.get("searchFilter"))

        # Get all rows from database a-z
        users = AuthUser.query.filter(
            getattr(AuthUser, search_filter).ilike(f"%{search_query}%")
        ).all()

        # Display results
        print("\n >>> Log ::: All users :\n", users)

        if len(users) <= 0:
            flash(f"No users found.", "warning")
            return render_template("/admin/u_management.html", users=[])
        else:
            return render_template("/admin/u_management.html", users=users)

    except Exception as e:
        print(f"\n >>> Log ::: There is an error while displaying data. {e}")
        flash(f"There is an error while displaying data. {e}", "danger")
        return render_template("/admin/u_management.html", users=[])


@blue_print.route("/admin/users/auth/edit/<email>")
@login_required
def view_auth_users(email):
    # Check if user information exists or not
    is_info_exists = db.session.query(
        db.exists().where(AuthUser.email == email)
    ).scalar()

    # Display existance check results
    print("\n >>> Log ::: User information check output :\n", is_info_exists)

    if is_info_exists == True:
        try:
            user = AuthUser.query.filter(AuthUser.email == email).one()

            return render_template(
                "/admin/u_profile_auth.html",
                user=user,
            )

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Getting user {email} has failed :\n", e)
            flash(f"Getting user {email} has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(f"\Getting user {email} has failed.", "danger")
        return redirect(request.referrer)


@blue_print.route("/admin/users/auth/edit", methods=["POST"])
@login_required
def edit_auth_users():
    new_user = AuthUser(
        first_name=request.form["fname"],
        last_name=request.form["lname"],
        mobile=request.form["mobile"],
        email=request.form["email"],
    )

    if db.session.query(db.exists().where(AuthUser.email == new_user.email)).scalar():
        temp_user = AuthUser.query.filter_by(email=form.email.data).first()
        db.session.add(new_user)
        db.session.commit()

    return manage_auth_users()


@blue_print.route("/admin/user-management/delete/<email>/")
@login_required
def delete_auth_user(email):
    # Check if user information exists or not
    is_info_exists = db.session.query(
        db.exists().where(AuthUser.email == email)
    ).scalar()

    # Display existance check results
    print("\n >>> Log ::: Admin information check output :\n", is_info_exists)

    if is_info_exists == True:
        try:
            delete_info_result = AuthUser.query.filter_by(email=email).delete()
            db.session.commit()

            # Display results
            print(
                "\n >>> Log ::: User information delete process output :\n",
                delete_info_result,
            )

            return redirect(url_for("routes.u_management"))

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Deleting user {token} has failed :\n", e)
            flash(f"Deleting user {token} has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(f"Deleting user {token} has failed.", "danger")
        return redirect(request.referrer)


# Normal Users


@blue_print.route("/admin/users/<option>")
@login_required
def display_users(option):
    try:
        if option == "all":
            users = User.query.order_by(User.created_at.desc()).all()
            destination = "u_all.html"

        if option == "new":
            users = (
                User.query.filter(User.status == 0)
                .order_by(User.created_at.desc())
                .all()
            )
            destination = "u_new.html"

        if option == "con":
            users = (
                User.query.filter(User.status == 1)
                .order_by(User.created_at.desc())
                .all()
            )
            destination = "u_confirmed.html"

        # Display results
        print("\n >>> Log ::: All users :\n", users)

        if len(users) <= 0:
            flash(f"No users found.", "warning")
            return render_template(f"/admin/{destination}", users=[])
        else:
            return render_template(f"/admin/{destination}", users=users)

    except Exception as e:
        flash(f"There is an error while displaying data. {e}", "danger")
        return render_template("/admin/u_all.html", users=[])


@blue_print.route("/admin/users/sort/option=<option>")
@login_required
def sort_users(option):
    users = User.query.all()

    try:
        if option == "atoz":
            users = User.query.order_by(
                User.first_name.asc(), User.last_name.asc()
            ).all()

        if option == "ztoa":
            users = User.query.order_by(
                User.first_name.desc(), User.last_name.desc()
            ).all()

        if option == "newest":
            users = User.query.order_by(User.created_at.desc()).all()

        if option == "oldest":
            users = User.query.order_by(User.created_at.asc()).all()

        # Display results
        print("\n >>> Log ::: All users :\n", users)

        if len(users) <= 0:
            flash(f"No users found.", "warning")
            return render_template("/admin/u_all.html", users=[])
        else:
            return render_template("/admin/u_all.html", users=users)

    except Exception as e:
        print(f"\n >>> Log ::: There is an error while displaying data. {e}")
        flash(f"There is an error while displaying data. {e}", "danger")
        return render_template("/admin/u_all.html", users=[])


@blue_print.route("/admin/users/search")
@login_required
def search_users():
    try:
        search_query = str(request.args.get("searchInp"))
        search_filter = str(request.args.get("searchFilter"))

        # Get all rows from database a-z
        users = User.query.filter(
            getattr(User, search_filter).ilike(f"%{search_query}%")
        ).all()

        # Display results
        print("\n >>> Log ::: All users :\n", users)

        if len(users) <= 0:
            flash(f"No users found.", "warning")
            return render_template("/admin/u_all.html", users=[])
        else:
            return render_template("/admin/u_all.html", users=users)

    except Exception as e:
        print(f"\n >>> Log ::: There is an error while displaying data. {e}")
        flash(f"There is an error while displaying data. {e}", "danger")
        return render_template("/admin/u_all.html", users=[])


@blue_print.route("/admin/user/<token>/info")
@login_required
def user_info(token):
    image_set = {}

    # Check if user information exists or not
    is_info_exists = db.session.query(
        db.exists().where(User.user_token == token)
    ).scalar()

    # Check if user images exists or not
    try:
        is_image_exists = os.path.join(c.IMAGE_DB_PATH, token)
    except Exception as e:
        is_image_exists = False

    # Display existance check results
    print("\n >>> Log ::: User information check output :\n", is_info_exists)
    print("\n >>> Log ::: User images check output :\n", is_image_exists)

    # Try to get images and info of given user token

    if is_info_exists == True and is_image_exists != False:
        try:
            user = User.query.filter(User.user_token == token).one()

            for img in os.listdir(is_image_exists):
                img_name, img_ext = os.path.splitext(secure_filename(img))

                # Read images and encode and decode to text so HTML can directly display them
                with open(f"{os.path.join(is_image_exists)}/{img}", "rb") as image_file:
                    image_set[img_name] = (base64.b64encode(image_file.read())).decode()

            return render_template("/admin/profile.html", user=user, images=image_set)

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Getting user {token} has failed :\n", e)
            flash(f"Getting user {token} has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(f"\Getting user {token} has failed.", "danger")
        return redirect(request.referrer)


@blue_print.route("/admin/user/<token>/status=<current_status>/")
@login_required
def update_status(token, current_status):
    # Check if user information exists or not
    is_info_exists = db.session.query(
        db.exists().where(User.user_token == token)
    ).scalar()

    # Display existance check results
    print("\n >>> Log ::: User information check output :\n", is_info_exists)

    if is_info_exists == True:
        try:
            user = User.query.filter_by(user_token=token).first()
            print(user)
            user.status = 1 if user.status == 0 else 0
            db.session.commit()

            # Display results
            print(
                "\n >>> Log ::: User status update results :\n",
                user,
            )

            user = db.session.query(User.status).filter(User.user_token == token).one()

            # Display results
            print(
                "\n >>> Log ::: New user status :\n",
                user.status,
            )

            flash(
                f"Status set to {'Vaccinated' if user.status == 1 else 'Not Vaccinated' }",
                "info",
            )

            return redirect(request.referrer)

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Updating user {token} status has failed :\n", e)
            flash(f"Updating user {token} status has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(f"Updating user {token} status has failed.", "danger")
        return redirect(request.referrer)


@blue_print.route("/admin/user/<token>/delete")
@login_required
def delete_user(token):
    # Check if user information exists or not
    is_info_exists = db.session.query(
        db.exists().where(User.user_token == token)
    ).scalar()

    # Check if user images exists or not
    try:
        is_image_exists = os.path.join(c.IMAGE_DB_PATH, token)
    except Exception as e:
        is_image_exists = False

    # Display existance check results
    print("\n >>> Log ::: User information check output :\n", is_info_exists)
    print("\n >>> Log ::: User images check output :\n", is_image_exists)

    if is_info_exists == True and is_image_exists != False:
        try:
            delete_info_result = User.query.filter_by(user_token=token).delete()
            db.session.commit()
            delete_image_result = shutil.rmtree(is_image_exists)

            # Display results
            print(
                "\n >>> Log ::: User information delete process output :\n",
                delete_info_result,
            )
            print(
                "\n >>> Log ::: User images delete process output :\n",
                delete_image_result,
            )

            return redirect(url_for("routes.unconfirmed_users"))

        except Exception as e:
            # Print and return exception
            print(f"\n >>> Log ::: Deleting user {token} has failed :\n", e)
            flash(f"Deleting user {token} has failed : {e}", "danger")
            return redirect(request.referrer)
    else:
        flash(f"Deleting user {token} has failed.", "danger")
        return redirect(request.referrer)
