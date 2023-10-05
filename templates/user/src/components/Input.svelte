<script>
    /**
     *
     * @component Input
     *
     * @props label (String): Input label.
     * @props options (Object): Input attributes.
     * @props value (String): Input value.
     * @props error (String): Form validation.
     */

    export let label;
    export let options = {};
    export let value = "";
    export let error = "";
</script>

<!-- Input -->
<div class="my-3">
    {#if label}
        <label for="" class="form-label form-label-lg text-primary fw-bold">
            {label}
        </label>
    {/if}

    <input
        type="text"
        {...options}
        bind:value
        class="form-control form-control-lg border border-2 rounded-1 border-dark"
    />

    {#if error}<div class="text-small fst-italic text-danger mt-2">
            {error}
        </div>
    {/if}
</div>
