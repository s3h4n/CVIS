<script>
    /**
     *
     * @component Select
     *
     * @props label (String): Select label.
     * @props options (Object): Select attributes.
     * @props items (List):  Select items (Options).
     * @props value (String): Selected value.
     * @props error (String): Form validation.
     *
     */

    export let label;
    export let options = {};
    export let items = [];
    export let value = "";
    export let error = "";
</script>

<!-- Select -->
<div class="my-3">
    {#if label}
        <label for="" class="form-label text-primary fw-bold">
            {label}
        </label>
    {/if}

    <select
        class="form-select form-select-lg border border-2 rounded-1 border-dark"
        {...options}
        bind:value
    >
        {#each items as item}
            <option value={item}>{item}</option>
        {/each}
    </select>

    {#if error}<div class="text-small fst-italic text-danger mt-2">
            {error}
        </div>
    {/if}
</div>
