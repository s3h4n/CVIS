<script>
    /**
     * This is the Home Page.
     */

    import { onMount } from "svelte";
    import QrScanner, { init } from "../components/QRScanner.svelte";
    import Button from "../components/Button.svelte";
    import PageTransistion from "../components/transistions/PageTransistion.svelte";
    import QrScanAnimation from "../components/animated/QrScan.svelte";

    onMount(init);

    let heading = "COVID-19 VACCINATION INFORMATION SYSTEM";
    let subHeading =
        "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Exlibero corrupti ducimus cum porro.";
</script>

<svelte:head>
    <title>CVIS | Home</title>
</svelte:head>

<svelte:component this={PageTransistion}>
    <main class="container my-5">
        <div class="row">
            <div class="col-lg-6 mb-5 order-lg-last">
                <svelte:component this={QrScanAnimation} />
            </div>
            <div class="col-lg-6">
                <h1 class="display-5 mt-lg-5">
                    {heading}
                </h1>
                <p class="text-primary lead  mt-3">
                    {subHeading}
                </p>
                <div class="col-md-4 mt-5 pt-5">
                    <QrScanner>
                        <Button label="Scan ID" />
                    </QrScanner>
                </div>
            </div>
        </div>
    </main>
</svelte:component>

<style>
</style>
