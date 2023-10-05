<script>
    /**
     * This is the Register Page.
     */

    import Input from "../Input.svelte";
    import Button from "../Button.svelte";
    import Select from "../Select.svelte";
    import Swal from "sweetalert2";
    import { push } from "svelte-spa-router";
    import axios from "axios";

    let form; // Form ID

    let formData = {
        firstName: "",
        lastName: "",
        dob: "",
        gender: "",
        email: "",
        mobile: "",
        addrLine1: "",
        addrLine2: "",
        town: "",
        uid: "",
        uidType: "",
        uidFront: "",
        uidBack: "",
        vacCount: "",
        vacFront: "",
        vacBack: "",
    };

    let formAttributes = {
        firstName: {
            type: "text",
            name: "firstName",
            max: "50",
            placeholder: "Ex: Sehan",
            style: "text-transform: capitalize;",
        },
        lastName: {
            type: "text",
            name: "lastName",
            max: "50",
            placeholder: "Ex: Weerasekara",
            style: "text-transform: capitalize;",
        },
        dob: {
            type: "date",
            name: "dob",
        },
        gender: {
            name: "gender",
        },
        email: {
            type: "email",
            name: "email",
            max: "50",
            placeholder: "Ex: sehan@example.com",
            style: "text-transform: lowercase;",
        },
        mobile: {
            type: "text",
            name: "mobile",
            max: "10",
            placeholder: "Ex: 07X XX XX XXX",
        },
        addrLine1: {
            type: "text",
            name: "addrLine1",
            max: "50",
            placeholder: "Ex: Thalpawila North",
            style: "text-transform: capitalize;",
        },
        addrLine2: {
            type: "text",
            name: "addrLine2",
            max: "50",
            placeholder: "Ex: Thalpawila",
            style: "text-transform: capitalize;",
        },
        town: {
            type: "text",
            name: "town",
            max: "50",
            placeholder: "Ex: Kekanadura",
            style: "text-transform: capitalize;",
        },
        uid: {
            type: "text",
            name: "uid",
            max: "12",
            placeholder: "Ex: 1234567891234",
        },
        uidType: {
            name: "uidType",
        },
        uidFront: {
            type: "file",
            name: "uidFront",
            capture: "environment",
            accept: "image/*",
        },
        uidBack: {
            type: "file",
            name: "uidBack",
            capture: "environment",
            accept: "image/*",
        },
        vacCount: {
            name: "vacCount",
        },
        vacFront: {
            type: "file",
            name: "vacFront",
            capture: "environment",
            accept: "image/*",
        },
        vacBack: {
            type: "file",
            name: "vacBack",
            capture: "environment",
            accept: "image/*",
        },
        submitButton: {
            type: "submit",
            name: "vacBack",
            class: "text-uppercase",
        },
    };

    let instructions = [
        "You must fill all the data of this form correctly.",
        "If you are under 16 and don't have a NIC/Passport, you can use your Birth Certificate number.",
        "Photographs must be clear and it must show required details.",
        "Re-check your data before submission.",
        "Forms with unclear/blured photographs will be instantly rejected.",
        "Forms that doesn't match-up with the photographs will also be rejected.",
        "Please save the QR code and the Token that you receive after registration.",
    ];

    let validationMsg = {
        firstName: "",
        lastName: "",
        dob: "",
        gender: "",
        email: "",
        mobile: "",
        addrLine1: "",
        addrLine2: "",
        town: "",
        uid: "",
        uidType: "",
        uidFront: "",
        uidBack: "",
        vacCount: "",
        vacFront: "",
        vacBack: "",
    };

    let validate = () => {
        let regexPatterns = {
            nic: /^[0-9]{12}|[0-9]{9}[vVxX]$/,
            passport: /^(?!^0+$)[a-zA-Z0-9]{3,20}$/,
            bc: /^[1-9]\d*$/,
            email: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
            mobile: /^(?:07)[0-9]{8}$/,
        };

        let errCount = 0;

        // First name
        if (formData.firstName.trim().length <= 0) {
            validationMsg.firstName = "Required.";
            errCount++;
        } else {
            validationMsg.firstName = "";
        }

        // Last name
        if (formData.lastName.trim().length <= 0) {
            validationMsg.lastName = "Required.";
            errCount++;
        } else {
            validationMsg.lastName = "";
        }

        // Address line 1
        if (formData.addrLine1.trim().length <= 0) {
            validationMsg.addrLine1 = "Required.";
            errCount++;
        } else {
            validationMsg.addrLine1 = "";
        }

        // Address line 2
        if (formData.addrLine2.trim().length <= 0) {
            validationMsg.addrLine2 = "Required.";
            errCount++;
        } else {
            validationMsg.addrLine2 = "";
        }

        // Town
        if (formData.town.trim().length <= 0) {
            validationMsg.town = "Required.";
            errCount++;
        } else {
            validationMsg.town = "";
        }

        // Date of birth
        if (formData.dob.trim().length <= 0) {
            validationMsg.dob = "Required.";
            errCount++;
        } else {
            validationMsg.dob = "";
        }

        // Gender
        if (formData.gender.trim().length <= 0) {
            validationMsg.gender = "Required.";
            errCount++;
        } else {
            validationMsg.gender = "";
        }

        // Email
        if (formData.email.trim().length <= 0) {
            validationMsg.email = "Required.";
            errCount++;
        } else if (regexPatterns.email.test(formData.email) === false) {
            validationMsg.email = "Invalid email address.";
            errCount++;
        } else {
            validationMsg.email = "";
        }

        // mobile
        if (formData.mobile.trim().length <= 0) {
            validationMsg.mobile = "Required.";
            errCount++;
        } else if (regexPatterns.mobile.test(formData.mobile) === false) {
            validationMsg.mobile = "Invalid mobile number.";
            errCount++;
        } else {
            validationMsg.mobile = "";
        }

        // UserID type
        if (formData.uidType.trim().length <= 0) {
            validationMsg.uidType = "Required.";
            errCount++;
        } else {
            validationMsg.uidType = "";
        }

        // UserID
        if (formData.uid.trim().length <= 0) {
            validationMsg.uid = "Required.";
            errCount++;
        } else if (formData.uidType === "NIC") {
            if (
                formData.uid.trim().length > 12 ||
                regexPatterns.nic.test(formData.uid) === false
            ) {
                validationMsg.uid = "Invalid NIC.";
                errCount++;
            } else {
                validationMsg.uid = "";
            }
        } else if (formData.uidType === "Passport") {
            if (regexPatterns.passport.test(formData.uid) === false) {
                validationMsg.uid = "Invalid Passport.";
                errCount++;
            } else {
                validationMsg.uid = "";
            }
        } else if (formData.uidType === "Birth Certificate") {
            if (regexPatterns.bc.test(formData.uid) === false) {
                validationMsg.uid = "Invalid Birth Certificate number.";
                errCount++;
            } else {
                validationMsg.uid = "";
            }
        }

        // UserID card front
        if (formData.uidFront.length <= 0) {
            validationMsg.uidFront = "Required.";
            errCount++;
        } else {
            validationMsg.uidFront = "";
        }

        // UserID card back
        if (formData.uidBack.length <= 0) {
            validationMsg.uidBack = "Required.";
            errCount++;
        } else {
            validationMsg.uidBack = "";
        }

        // Vaccine count
        if (formData.vacCount.trim().length <= 0) {
            validationMsg.vacCount = "Required.";
            errCount++;
        } else {
            validationMsg.vacCount = "";
        }

        // Vaccine card front
        if (formData.vacFront.length <= 0) {
            validationMsg.vacFront = "Required.";
            errCount++;
        } else {
            validationMsg.vacFront = "";
        }

        // Vaccine card back
        if (formData.vacBack.length <= 0) {
            validationMsg.vacBack = "Required.";
            errCount++;
        } else {
            validationMsg.vacBack = "";
        }

        return errCount;
    };

    let registrationHandler = async () => {
        if (validate() <= 0) {
            // Backend end-point
            let fetchURL = "/api/user-registration?";

            // Collect all form data
            let data = new FormData(form);

            try {
                let response = await axios.post(fetchURL, data, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });

                let responseData = response.data;

                console.log(responseData);

                if (responseData["status"] === "true") {
                    // Display alert
                    Swal.fire({
                        title: "Registration Successfull!",
                        text: responseData["message"],
                        icon: "success",
                        confirmButtonText: "Ok",
                    }).then(() => {
                        push("/");
                    });
                } else {
                    Swal.fire({
                        title: "Registration Failed!",
                        text: responseData["message"],
                        icon: "error",
                        confirmButtonText: "Ok",
                    });
                }
            } catch (err) {
                Swal.fire({
                    title: "Registration Failed!",
                    text: `${err}.`,
                    icon: "error",
                    confirmButtonText: "Ok",
                }).then(() => {
                    console.error("Error: ", err);
                });
            }
        }
    };
</script>

<form
    bind:this={form}
    class="row"
    on:submit|preventDefault={registrationHandler}
    on:input={validate}
>
    <div class="col-lg-4 mb-5 order-lg-last">
        <h2 class="text-primary mb-5 ps-lg-5">Instructions and Rules</h2>
        <ul class="ps-lg-5">
            {#each instructions as ins}
                <li class="mb-2">{@html ins}</li>
            {/each}
        </ul>
    </div>
    <div class="col-lg-8 float-end">
        <!-- Personal -->
        <div class="row">
            <div class="col-lg-6">
                <Input
                    label="First Name"
                    options={formAttributes.firstName}
                    bind:value={formData.firstName}
                    error={validationMsg.firstName}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Last Name"
                    options={formAttributes.lastName}
                    bind:value={formData.lastName}
                    error={validationMsg.lastName}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Date of Birth"
                    options={formAttributes.dob}
                    bind:value={formData.dob}
                    error={validationMsg.dob}
                />
            </div>
            <div class="col-lg-6">
                <Select
                    label="Gender"
                    options={formAttributes.gender}
                    items={["Male", "Female"]}
                    bind:value={formData.gender}
                    error={validationMsg.gender}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Email Address"
                    options={formAttributes.email}
                    bind:value={formData.email}
                    error={validationMsg.email}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Mobile Number"
                    options={formAttributes.mobile}
                    bind:value={formData.mobile}
                    error={validationMsg.mobile}
                />
            </div>
        </div>

        <!-- Contact -->
        <div class="row">
            <div class="col-lg-4">
                <Input
                    label="Address Line 01"
                    options={formAttributes.addrLine1}
                    bind:value={formData.addrLine1}
                    error={validationMsg.addrLine1}
                />
            </div>
            <div class="col-lg-4">
                <Input
                    label="Address Line 02"
                    options={formAttributes.addrLine2}
                    bind:value={formData.addrLine2}
                    error={validationMsg.addrLine2}
                />
            </div>
            <div class="col-lg-4">
                <Input
                    label="Hometown"
                    options={formAttributes.town}
                    bind:value={formData.town}
                    error={validationMsg.town}
                />
            </div>
        </div>

        <!-- Identity -->
        <div class="row">
            <div class="col-lg-6">
                <Input
                    label="{formData.uidType === ''
                        ? 'NIC/Passport/Birth Certificate'
                        : formData.uidType} Number"
                    options={formAttributes.uid}
                    bind:value={formData.uid}
                    error={validationMsg.uid}
                />
            </div>
            <div class="col-lg-6">
                <Select
                    label="Identity Type"
                    options={formAttributes.uidType}
                    items={["NIC", "Passport", "Birth Certificate"]}
                    bind:value={formData.uidType}
                    error={validationMsg.uidType}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Photograph of {formData.uidType} (Front Side)"
                    options={formAttributes.uidFront}
                    bind:value={formData.uidFront}
                    error={validationMsg.uidFront}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Photograph of {formData.uidType} (Back Side)"
                    options={formAttributes.uidBack}
                    bind:value={formData.uidBack}
                    error={validationMsg.uidBack}
                />
            </div>
        </div>

        <!-- Vaccine -->
        <div class="row">
            <div class="col-lg-6">
                <Select
                    label="Number of Vaccinations"
                    options={formAttributes.vacCount}
                    items={["1", "2", "3", "4"]}
                    bind:value={formData.vacCount}
                    error={validationMsg.vacCount}
                />
            </div>
            <div class="col-lg-6" />
            <div class="col-lg-6">
                <Input
                    label="Photograph of Vaccine Card (Front Side)"
                    options={formAttributes.vacFront}
                    bind:value={formData.vacFront}
                    error={validationMsg.vacFront}
                />
            </div>
            <div class="col-lg-6">
                <Input
                    label="Photograph of Vaccine Card (Back Side)"
                    options={formAttributes.vacBack}
                    bind:value={formData.vacBack}
                    error={validationMsg.vacBack}
                />
            </div>
        </div>

        <hr class="my-5" />

        <!-- Submit -->
        <div class="row">
            <div class="col-lg-6" />
            <div class="col-lg-6">
                <Button
                    label="Register"
                    options={formAttributes.submitButton}
                />
            </div>
        </div>
    </div>
</form>
