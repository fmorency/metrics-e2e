<script lang="ts">
  import MetricsPage from "$lib/components/MetricsPage.svelte";
  import type {PageProps} from "../../../.svelte-kit/types/src/routes/disk/$types";
  import {configs} from "./config";

  let { data }: PageProps = $props();
</script>

<MetricsPage title="Disk" data={data.data} {configs} />
