<script>
    /**
     *
     * @component Page Transistion
     *
     * @props refresh(String): Key to re-play transistion.
     *
     */

    import { fly } from "svelte/transition";
</script>

<!-- Page Transistion -->
<div in:fly={{ y: -100, duration: 1000 }}>
    <slot />
</div>
