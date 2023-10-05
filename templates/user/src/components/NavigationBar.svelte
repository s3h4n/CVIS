<script>
    /**
     *
     * @component Navigaition Bar
     *
     * @props lnavBrand(String): Navigation bar brand name.
     * @props sideBarTitle(String): Navigation bar responsive sidebar title.
     * @props navItems(List): Navigation bar links.
     * @props currentURL(String): Navigation bar current active page.
     *
     */

    import { link } from "svelte-spa-router";

    export let navBrand;
    export let sideBarTitle;
    export let navItems = [];
    export let currentURL;

    let yAxis;
</script>

<!-- Navigation Bar -->
<nav
    class="navbar navbar-expand-lg py-3 sticky-top text-uppercase navbar-light
    {yAxis <
    50
        ? ''
        : 'bg-light shadow-sm'}"
>
    <div class="container">
        <a class="navbar-brand text-primary fw-bold fs-3 ms-3 me-3" href="/">
            {navBrand}
        </a>

        <button
            class="navbar-toggler text-primary shadow-none border-0"
            type="button"
            data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasNavbar"
            aria-controls="offcanvasNavbar"
        >
            <span class="navbar-toggler-icon text-primary" />
        </button>

        <div
            class="offcanvas offcanvas-end"
            tabindex="-1"
            id="offcanvasNavbar"
            aria-labelledby="offcanvasNavbarLabel"
        >
            <div class="offcanvas-header ms-3 me-3">
                <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
                    {sideBarTitle}
                </h5>

                <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="offcanvas"
                    aria-label="Close"
                />
            </div>

            <div class="offcanvas-body">
                <ul class="navbar-nav justify-content-end flex-grow-1">
                    {#each navItems as item}
                        <li
                            class="nav-item text-dark fw-semibold ms-lg-5 ms-3 me-3"
                        >
                            <a
                                data-bs-target="#offcanvasNavbar"
                                data-bs-dismiss="offcanvas"
                                aria-label="Close"
                                class="nav-link {currentURL === item.url
                                    ? 'active text-primary border-3 border-bottom border-primary'
                                    : ''}"
                                href={item.url}
                                use:link
                            >
                                {item.text}
                            </a>
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
    </div>
</nav>

<svelte:window bind:scrollY={yAxis} />
