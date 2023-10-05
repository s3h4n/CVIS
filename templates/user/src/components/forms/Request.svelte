<script>
    /**
     * This is the Request Token Page.
     */

    import Input from "../Input.svelte";
    import Button from "../Button.svelte";
    import Select from "../Select.svelte";
    import Request from "../animated/Request.svelte";
    import Swal from "sweetalert2";
    import { push } from "svelte-spa-router";
    import axios from "axios";

    let form; // Form ID

    let formData = {
        email: "",
        uid: "",
        uidType: "",
    };

    let formAttributes = {
        email: {
            type: "email",
            name: "email",
            max: "50",
            placeholder: "Ex: sehan@example.com",
            style: "text-transform: lowercase;",
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
        submitButton: {
            type: "submit",
        },
    };

    let validationMsg = {
        email: "",
        uid: "",
        uidType: "",
    };

    let validate = () => {
        let regexPatterns = {
            nic: /^[0-9]{12}|[0-9]{9}[vVxX]$/,
            passport: /^(?!^0+$)[a-zA-Z0-9]{3,20}$/,
            bc: /^[1-9]\d*$/,
            email: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        };

        let errCount = 0;

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
                validationMsg.uid = "Invalid Birth Certificate.";
                errCount++;
            } else {
                validationMsg.uid = "";
            }
        }
        return errCount;
    };

    let handler = async () => {
        if (validate() <= 0) {
            let fetchURL = "/api/request-id?";

            let data = new FormData(form);

            try {
                let response = await axios.post(fetchURL, data, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });

                let responseData = response.data;

                //console.log("Response: ", response.data);

                let responsejson = JSON.stringify(response.data); // to JSON object

                if (responseData["status"] === "false") {
                    Swal.fire({
                        title: "Error!",
                        text: responseData["message"],
                        icon: "error",
                        confirmButtonText: "Ok",
                    });
                } else {
                    await Swal.fire({
                        title: "Here is Your QR!",
                        imageUrl:
                            "https://api.qrserver.com/v1/create-qr-code/?data=" +
                            responsejson +
                            "&amp;size=150x150",
                        imageWidth: 200,
                        imageHeight: 200,
                        imageAlt: "QR Code",
                        confirmButtonText: "Ok",
                        showLoaderOnConfirm: true,
                    }).then(() => {
                        push("/");
                    });
                }
            } catch (err) {
                Swal.fire({
                    title: "Requesting ID Failed!",
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
    on:submit|preventDefault={handler}
    on:input={validate}
>
    <div class="col-lg-6 mb-5 order-lg-last">
        <Request />
    </div>
    <div class="col-lg-6 float-end">
        <h1 class="display-5 mb-5">Request ID</h1>
        <!-- Identity -->
        <div class="row">
            <div class="col-lg-8">
                <Input
                    label="{formData.uidType === ''
                        ? 'NIC/Passport/Birth Certificate'
                        : formData.uidType} Number"
                    options={formAttributes.uid}
                    bind:value={formData.uid}
                    error={validationMsg.uid}
                />
            </div>
            <div class="col-lg-4">
                <Select
                    label="Identity Type"
                    options={formAttributes.uidType}
                    items={["NIC", "Passport", "Birth Certificate"]}
                    bind:value={formData.uidType}
                    error={validationMsg.uidType}
                />
            </div>
            <div class="col-lg-8">
                <Input
                    label="Email Address"
                    options={formAttributes.email}
                    bind:value={formData.email}
                    error={validationMsg.email}
                />
            </div>

            <hr class="my-5" />

            <div class="col-lg-8">
                <Button label="Request" options={formAttributes.submitButton} />
            </div>
        </div>
    </div>
</form>
