<script lang="ts">
  import MetricsPage from "$lib/components/MetricsPage.svelte";
  import type {PageProps} from "../../../.svelte-kit/types/src/routes/blockchain/$types";
  import {configs} from "./config";

  let { data }: PageProps = $props();
</script>

<MetricsPage title="Blockchain" data={data.data} {configs} />
