<script>
    /**
     * This is the 404 Page.
     */

    import PageTransistion from "../components/transistions/PageTransistion.svelte";
    import FourZeroFour from "../components/animated/FourZeroFour.svelte";
</script>

<svelte:head>
    <title>CVIS | 404 Not Found</title>
</svelte:head>

<svelte:component this={PageTransistion}>
    <main class="container ms-auto">
        <div class="row">
            <div class="col-lg-3" />
            <div class="col-lg-6">
                <svelte:component this={FourZeroFour} />
            </div>
            <div class="col-lg-3" />
        </div>
    </main>
</svelte:component>
