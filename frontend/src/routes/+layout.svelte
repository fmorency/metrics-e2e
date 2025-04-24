<script lang="ts">
  import '../app.css';
  import { Navigation, AppBar, Segment } from '@skeletonlabs/skeleton-svelte';
  import HardDrive from "carbon-pictograms-svelte/lib/HardDrive.svelte";
  import Network from "carbon-pictograms-svelte/lib/Network.svelte";
  import Desktop from "carbon-pictograms-svelte/lib/Desktop.svelte";
  import Websites from "carbon-pictograms-svelte/lib/Websites.svelte";
  import Kubernetes from "carbon-pictograms-svelte/lib/Kubernetes.svelte";
  import CloudObjectStorage from "carbon-pictograms-svelte/lib/CloudObjectStorage.svelte";
  import GpuComputing from "carbon-pictograms-svelte/lib/GpuComputing.svelte";
  import Blockchain from "carbon-pictograms-svelte/lib/Blockchain.svelte";
  import { page } from '$app/state';
  import { goto } from '$app/navigation'
  import LightSwitch from "$lib/components/LightSwitch.svelte";
  import {mode} from '$lib/stores/theme';

  let isDark = $derived($mode === 'dark');
  let ready = $state(false);
  $effect(() => {
    return mode.subscribe(() => {
      ready = true;
    });
  });

  let { children } = $props();

  const menuItems = [
    { href: '/blockchain', title: 'Blockchain', icon: Blockchain },
    { href: '/system', title: 'System', icon: Desktop },
    { href: '/disk', title: 'Disk', icon: HardDrive },
    { href: '/network', title: 'Network', icon: Network },
    { href: '/web', title: 'Web', icon: Websites },
    { href: '/object_storage', title: 'Object Storage', icon: CloudObjectStorage },
    { href: '/kubernetes', title: 'Kubernetes', icon: Kubernetes },
    { href: '/gpu', title: 'GPU', icon: GpuComputing }
  ];

  const intervalOptions: { label: string; value: TimeInterval }[] = [
    { label: '1 Year', value: '1 year' },
    { label: '1 Month', value: '1 month' },
    { label: '1 Week', value: '1 week' },
    { label: '1 Day', value: '1 day' },
    { label: '1 Hour', value: '1 hour' },
    { label: '1 Minute', value: '1 minute' },
  ];

  const defaultInterval: TimeInterval = '1 day'
  let selectedInterval: TimeInterval = $state(page.url.searchParams.get('interval') as TimeInterval || defaultInterval)

  $effect(() => {
    const urlInterval = page.url.searchParams.get('interval') as TimeInterval || defaultInterval;
    if (selectedInterval !== urlInterval) {
      goto(`${page.url.pathname}?interval=${selectedInterval}`);
    }
  });
</script>

{#if ready}
<div class="flex flex-col h-screen overflow-hidden">
  <AppBar>
    {#snippet trail()}
      <Segment value={selectedInterval} name="interval" onValueChange={(e) => (selectedInterval = e.value as TimeInterval)} indicatorBg="bg-secondary-500" indicatorText="text-surface-900">
        {#each intervalOptions as option (option.value)}
            <Segment.Item value={option.value}>{option.label}</Segment.Item>
        {/each}
      </Segment>
    {/snippet}
    {#snippet lead()}
      <div class="relative">
        <a href="/" class="inline-block">
          <img src={isDark ? "/manifest_dark.svg" : "/manifest_light.svg"} alt="Logo" class="h-14" />
        </a>
      </div>
    {/snippet}
  </AppBar>

  <div class="card border-surface-100-900 grid w-full grid-cols-[auto_1fr] border-[1px] flex-1 overflow-hidden">
    <Navigation.Rail>
      {#snippet tiles()}
        {#each menuItems as tile}
          <Navigation.Tile href={tile.href} title={tile.title} selected={page.url.pathname === tile.href} classes={page.url.pathname === tile.href ? 'bg-secondary-500 text-surface-900' : ''}><tile.icon /></Navigation.Tile>
        {/each}
      {/snippet}

      {#snippet footer()}
        <LightSwitch />
      {/snippet}
    </Navigation.Rail>

    <div class="overflow-y-auto">
      {@render children?.()}
    </div>
  </div>
</div>
{/if}