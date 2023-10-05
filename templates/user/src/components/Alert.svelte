<script>
    /**
     *
     * @component Alert
     *
     * @props color (String): Alert color.
     *
     */

    export let color = "";
</script>

<!-- Alert -->
<div>
    <div class="alert alert-{color} text-wrap text-break" role="alert">
        <slot />
    </div>
</div>
