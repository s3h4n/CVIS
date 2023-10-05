<script>
    /**
     *
     * @component Secondary Button
     *
     * @props label (String): Button text.
     * @props options (Object): Button attributes.
     * @props click (function): Button onclick event.
     *
     */

    export let label;
    export let options = {};
    export let click = null;
</script>

<!-- Button -->
<div class="my-3">
    <button
        type="button"
        {...options}
        class="btn p-3 bg-light text-primary border border-2 rounded-1 border-primary text-uppercase w-100"
        on:click={click}
    >
        {label}
    </button>
</div>
