<script lang="ts">
  import {Switch} from '@skeletonlabs/skeleton-svelte';
  import Light from 'carbon-icons-svelte/lib/Light.svelte';
  import AsleepFilled from 'carbon-icons-svelte/lib/AsleepFilled.svelte';
  import {mode} from '$lib/stores/theme';

  let isDark = $derived($mode === 'dark');
  let ready = $state(false);

  $effect(() => {
    return mode.subscribe(() => {
      ready = true;
    });
  });

  $effect(() => {
    if (ready) {
      mode.set(isDark ? 'dark' : 'light');
    }
  });


</script>

{#if ready}
  <Switch checked={!isDark} onCheckedChange={(e) => (isDark = !e.checked)}>
    {#snippet inactiveChild()}<AsleepFilled />{/snippet}
    {#snippet activeChild()}<Light />{/snippet}
  </Switch>
{/if}