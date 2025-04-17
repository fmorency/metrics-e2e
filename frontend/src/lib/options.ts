import type {ChartConfig} from "./types";
import {ScaleTypes} from "@carbon/charts-svelte";

export function getChartOptions(config: ChartConfig) {
  return {
    title: config.title,
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
    theme: 'g100',
    color: {
      gradient: {
        enabled: true
      }
    },
    points: {
      enabled: false
    },
    legend: {
      position: 'bottom'
    }
  };
}