import type {ChartConfig, ChartDataPoint} from "./types";
import {ScaleTypes} from "@carbon/charts-svelte";

export function getChartOptions(config: ChartConfig, latest?: ChartDataPoint) {
  return {
    title:`${config.title}: ${latest?.value}`,
    axes: {
      bottom: {
        title: 'Timestamp',
        mapsTo: 'date',
        scaleType: ScaleTypes.TIME,
      },
      left: {
        mapsTo: 'value',
        title: config.yAxisTitle,
        scaleType: ScaleTypes.LINEAR,
      }
    },
    curve: 'curveMonotoneX',
    includeZero: false,
    height: '400px',
    color: {
      gradient: {
        enabled: true
      },
      scale: {
        [config.id]: '#E5703D'
      }
    },
    points: {
      enabled: false
    },
    legend: {
      enabled: false
    },
    toolbar: {
      enabled: false
    },
    grid: {
      x: {
        enabled: false
      }
    },
  };
}