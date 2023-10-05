<script>
    /**
     *
     * @component Modal
     *
     * @props id (String): Modal id attribute.
     * @props closeBtnClick: Close button onlick event.
     *
     */

    export let id;
    export let closeBtnClick;
</script>

<!-- Modal -->
<div
    class="modal fade"
    {id}
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="staticBackdropLabel"
    aria-hidden="true"
>
    <div class="modal-dialog ">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title text-dark" id="staticBackdropLabel">
                    <slot name="header" />
                </h5>

                <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                    on:click={closeBtnClick}
                />
            </div>

            <div class="modal-body">
                <slot name="body" />
            </div>

            <div class="modal-footer">
                <slot name="footer" />
            </div>
        </div>
    </div>
</div>
