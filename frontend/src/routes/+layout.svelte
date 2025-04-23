<script lang="ts">
  import '../app.css';
  import { Navigation, AppBar } from '@skeletonlabs/skeleton-svelte';
  import HardDrive from "carbon-pictograms-svelte/lib/HardDrive.svelte";
  import HomeFront from "carbon-pictograms-svelte/lib/HomeFront.svelte";
  import Network from "carbon-pictograms-svelte/lib/Network.svelte";
  import Desktop from "carbon-pictograms-svelte/lib/Desktop.svelte";
  import Websites from "carbon-pictograms-svelte/lib/Websites.svelte";
  import Kubernetes from "carbon-pictograms-svelte/lib/Kubernetes.svelte";
  import CloudObjectStorage from "carbon-pictograms-svelte/lib/CloudObjectStorage.svelte";
  import GpuComputing from "carbon-pictograms-svelte/lib/GpuComputing.svelte";
  import Blockchain from "carbon-pictograms-svelte/lib/Blockchain.svelte";
</script>

<div class="flex flex-col h-screen overflow-hidden">
  <AppBar>
    {#snippet headline()}
      <div class="relative">
        <a href="/" class="inline-block">
          <img src="/manifest.svg" alt="Logo" class="h-14" />
        </a>
      </div>
    {/snippet}
  </AppBar>

  <div class="card border-surface-100-900 grid w-full grid-cols-[auto_1fr] border-[1px] flex-1 overflow-hidden">
    <Navigation.Rail>
      {#snippet tiles()}
        <Navigation.Tile href="/blockchain" title="Blockchain"><Blockchain /></Navigation.Tile>
        <Navigation.Tile href="/system" title="System"><Desktop /></Navigation.Tile>
        <Navigation.Tile href="/disk" title="Disk"><HardDrive /></Navigation.Tile>
        <Navigation.Tile href="/network" title="Network"><Network /></Navigation.Tile>
        <Navigation.Tile href="/web" title="Web"><Websites /></Navigation.Tile>
        <Navigation.Tile href="/object_storage" title="Object Storage"><CloudObjectStorage /></Navigation.Tile>
        <Navigation.Tile href="/kubernetes" title="kubernetes"><Kubernetes /></Navigation.Tile>
        <Navigation.Tile href="/gpu" title="GPU"><GpuComputing /></Navigation.Tile>
      {/snippet}
    </Navigation.Rail>

    <div class="overflow-y-auto">
      <slot />
    </div>
  </div>
</div>
