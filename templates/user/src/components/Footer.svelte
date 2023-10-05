<script>
    /**
     *
     * @component Footer
     *
     * @props footerBrand (String): Footer text.
     *
     */

    export let footerBrand;
</script>

<!-- Footer -->
<footer class="py-1 mt-auto ">
    <hr />
    <p class="text-center text-muted mt-3">
        © {new Date().getFullYear()}
        {footerBrand}
    </p>
</footer>
