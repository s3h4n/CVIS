<script>
    /**
     *
     * @component Check Box
     *
     * @props label (String): Checkbox label.
     * @props options (Object): Input attributes.
     * @props checked (bool): Checked or not.
     */

    export let label;
    export let options = {};
    export let checked = false;
</script>

<!-- Input -->
<div class="form-check my-3">
    <input {...options} type="checkbox" class="form-check-input" bind:checked />

    {#if label}
        <label class="form-check-label" for="">
            {@html label}
        </label>
    {/if}
</div>
