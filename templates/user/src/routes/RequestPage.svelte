<script>
    /**
     * This is the Request Token Page.
     */

    import PageTransistion from "../components/transistions/PageTransistion.svelte";
    import Request from "../components/forms/Request.svelte";
</script>

<svelte:head>
    <title>CVIS | Request ID</title>
</svelte:head>

<svelte:component this={PageTransistion}>
    <main class="container my-5">
        <svelte:component this={Request} />
    </main>
</svelte:component>

<style>
</style>
