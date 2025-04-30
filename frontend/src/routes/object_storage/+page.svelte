<script lang="ts">
  import MetricsPage from "$lib/components/MetricsPage.svelte";
  import type {PageProps} from "../../../.svelte-kit/types/src/routes/object_storage/$types";
  import {configs} from "./config";

  let { data }: PageProps = $props();
</script>

<MetricsPage title="Object Storage" data={data.data} {configs} />
