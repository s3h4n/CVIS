<script>
    /**
     * This is the Register Page.
     */

    import PageTransistion from "../components/transistions/PageTransistion.svelte";
    import Register from "../components/forms/Register.svelte";
</script>

<svelte:head>
    <title>CVIS | Register</title>
</svelte:head>

<svelte:component this={PageTransistion}>
    <main class="container my-5">
        <h1 class="display-5 mb-5">New User Registration</h1>
        <svelte:component this={Register} />
    </main>
</svelte:component>

<style>
</style>
