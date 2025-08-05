import React, { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

declare global {
  interface Window {
    Chart: any;
  }
}

interface ChartData {
  projections: any[];
  sensitivity_analysis: any[];
  scenarios: any;
}

export const AnalysisCharts: React.FC = () => {
  const projectionChartRef = useRef<HTMLCanvasElement>(null);
  const sensitivityChartRef = useRef<HTMLCanvasElement>(null);
  const scenarioChartRef = useRef<HTMLCanvasElement>(null);

  // Store chart data persistently
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [chartsInitialized, setChartsInitialized] = useState(false);
  const [activeTab, setActiveTab] = useState('projection');

  // Store chart instances
  const chartInstances = useRef<{
    projection?: any;
    sensitivity?: any;
    scenario?: any;
  }>({});

  useEffect(() => {
    // Load Chart.js if not already loaded
    if (typeof window !== 'undefined' && !window.Chart) {
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
      script.onload = () => {
        setChartsInitialized(true);
        // Initialize all charts after Chart.js loads
        setTimeout(() => {
          initializeAllCharts();
        }, 100);
      };
      document.head.appendChild(script);
    } else if (window.Chart && !chartsInitialized) {
      setChartsInitialized(true);
      // Initialize all charts
      setTimeout(() => {
        initializeAllCharts();
      }, 100);
    }

    // Listen for DCF calculation results to update charts
    const handleDCFResults = (event: CustomEvent) => {
      const { projections, sensitivity_analysis, scenarios } = event.detail;
      const newChartData = {
        projections: projections || [],
        sensitivity_analysis: sensitivity_analysis || [],
        scenarios: scenarios || {}
      };

      setChartData(newChartData);

      // Update all charts immediately when data is received
      if (chartsInitialized) {
        setTimeout(() => {
          updateAllCharts(newChartData);
        }, 100);
      }
    };

    // Listen for company data fetch to clear charts
    const handleCompanyDataFetch = () => {
      setChartData(null);
      if (chartsInitialized) {
        setTimeout(() => {
          initializeAllCharts();
        }, 100);
      }
    };

    window.addEventListener('dcfResultsCalculated', handleDCFResults as EventListener);
    window.addEventListener('companyDataFetched', handleCompanyDataFetch as EventListener);

    return () => {
      window.removeEventListener('dcfResultsCalculated', handleDCFResults as EventListener);
      window.removeEventListener('companyDataFetched', handleCompanyDataFetch as EventListener);
    };
  }, [chartsInitialized]);

  // Update charts when data changes or tab switches
  useEffect(() => {
    if (chartData && chartsInitialized) {
      // Add delay to ensure canvas elements are visible
      setTimeout(() => {
        updateAllCharts(chartData);
      }, 100);
    }
  }, [chartData, chartsInitialized, activeTab]);

  const initializeAllCharts = () => {
    if (!window.Chart) return;

    // Initialize all charts with empty data
    createProjectionChart([]);
    createSensitivityChart([]);
    createScenarioChart({});
  };

  const updateAllCharts = (data: ChartData) => {
    createProjectionChart(data.projections);
    createSensitivityChart(data.sensitivity_analysis);
    createScenarioChart(data.scenarios);
  };

  const destroyChart = (chartRef: React.RefObject<HTMLCanvasElement | null>) => {
    if (chartRef.current && (chartRef.current as any).chart) {
      (chartRef.current as any).chart.destroy();
      (chartRef.current as any).chart = null;
    }
  };

  const createProjectionChart = (data: any[]) => {
    // Check if canvas element is visible and ready
    if (!projectionChartRef.current || !window.Chart) return;

    const canvas = projectionChartRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Ensure canvas has dimensions
    if (canvas.offsetWidth === 0 || canvas.offsetHeight === 0) {
      // Retry after a short delay if canvas is not visible
      setTimeout(() => createProjectionChart(data), 200);
      return;
    }

    destroyChart(projectionChartRef);

    const hasData = data && data.length > 0;
    const years = hasData ? data.map(d => `Year ${d.year}`) : ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'];
    const fcfData = hasData ? data.map(d => d.fcf) : [0, 0, 0, 0, 0];
    const pvData = hasData ? data.map(d => d.present_value) : [0, 0, 0, 0, 0];

    const chart = new window.Chart(ctx, {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
            label: 'Free Cash Flow',
            data: fcfData,
            borderColor: 'hsl(215, 28%, 17%)', // Dark slate
            backgroundColor: 'hsla(215, 28%, 17%, 0.1)', // Dark slate with transparency
            tension: 0.1,
            fill: true
          },
          {
            label: 'Present Value',
            data: pvData,
            borderColor: 'hsl(215, 16%, 47%)', // Medium slate
            backgroundColor: 'hsla(215, 16%, 47%, 0.1)', // Medium slate with transparency
            tension: 0.1,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Value ($M)'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: hasData ? 'Cash Flow Projections' : 'Cash Flow Projections (No Data)'
          },
          legend: {
            display: true,
            position: 'bottom'
          }
        }
      }
    });

    (projectionChartRef.current as any).chart = chart;
    chartInstances.current.projection = chart;
  };

  const createSensitivityChart = (data: number[]) => {
    // Check if canvas element is visible and ready
    if (!sensitivityChartRef.current || !window.Chart) return;

    const canvas = sensitivityChartRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Ensure canvas has dimensions
    if (canvas.offsetWidth === 0 || canvas.offsetHeight === 0) {
      // Retry after a short delay if canvas is not visible
      setTimeout(() => createSensitivityChart(data), 200);
      return;
    }

    destroyChart(sensitivityChartRef);

    const hasData = data && data.length >= 3;
    const labels = ['WACC -1%', 'Base Case', 'WACC +1%'];
    const values = hasData ? data.slice(0, 3) : [0, 0, 0];

    const chart = new window.Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Intrinsic Value',
          data: values,
          backgroundColor: [
            'hsla(215, 28%, 17%, 0.8)', // Dark slate
            'hsla(215, 16%, 47%, 0.8)', // Medium slate
            'hsla(215, 14%, 65%, 0.8)'  // Light slate
          ],
          borderColor: [
            'hsl(215, 28%, 17%)', // Dark slate
            'hsl(215, 16%, 47%)', // Medium slate
            'hsl(215, 14%, 65%)'  // Light slate
          ],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Value per Share ($)'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: hasData ? 'WACC Sensitivity Analysis' : 'WACC Sensitivity Analysis (No Data)'
          },
          legend: {
            display: false
          }
        }
      }
    });

    (sensitivityChartRef.current as any).chart = chart;
    chartInstances.current.sensitivity = chart;
  };

  const createScenarioChart = (scenarios: any) => {
    // Check if canvas element is visible and ready
    if (!scenarioChartRef.current || !window.Chart) return;

    const canvas = scenarioChartRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Ensure canvas has dimensions
    if (canvas.offsetWidth === 0 || canvas.offsetHeight === 0) {
      // Retry after a short delay if canvas is not visible
      setTimeout(() => createScenarioChart(scenarios), 200);
      return;
    }

    destroyChart(scenarioChartRef);

    // Check if we have meaningful scenario data
    const hasData = scenarios && Object.keys(scenarios).length > 0;

    let chartData, labels;
    if (hasData) {
      // Use actual scenario data if available
      labels = Object.keys(scenarios);
      chartData = Object.values(scenarios).map((value: any) =>
        typeof value === 'object' && value.intrinsic_value ? value.intrinsic_value : value
      );
    } else {
      // Default placeholder data
      labels = ['Conservative', 'Base Case', 'Optimistic'];
      chartData = [0, 0, 0];
    }

    // Monochrome slate palette for chart segments
    const slateColors = [
      'hsla(215, 28%, 17%, 0.8)', // Darkest slate
      'hsla(215, 20%, 35%, 0.8)', // Dark slate
      'hsla(215, 16%, 47%, 0.8)', // Medium slate
      'hsla(215, 14%, 65%, 0.8)', // Light slate
      'hsla(214, 32%, 85%, 0.8)'  // Very light slate
    ];

    const slateBorders = [
      'hsl(215, 28%, 17%)', // Darkest slate
      'hsl(215, 20%, 35%)', // Dark slate
      'hsl(215, 16%, 47%)', // Medium slate
      'hsl(215, 14%, 65%)', // Light slate
      'hsl(214, 32%, 85%)'  // Very light slate
    ];

    const chart = new window.Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: chartData,
          backgroundColor: slateColors.slice(0, labels.length),
          borderColor: slateBorders.slice(0, labels.length),
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: hasData ? 'Scenario Analysis' : 'Scenario Analysis (No Data)'
          },
          legend: {
            position: 'bottom'
          }
        }
      }
    });

    (scenarioChartRef.current as any).chart = chart;
    chartInstances.current.scenario = chart;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
          </svg>
          <span>Analysis Charts</span>
          {chartData && (
            <span className="text-sm text-muted-foreground ml-2">
              (Data Available)
            </span>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs
          defaultValue="projection"
          className="w-full"
          onValueChange={(value) => {
            setActiveTab(value);
            // Re-render charts when tab becomes visible
            if (chartData && chartsInitialized) {
              setTimeout(() => {
                if (value === 'projection') createProjectionChart(chartData.projections);
                if (value === 'sensitivity') createSensitivityChart(chartData.sensitivity_analysis);
                if (value === 'scenarios') createScenarioChart(chartData.scenarios);
              }, 50);
            }
          }}
        >
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="projection">Projections</TabsTrigger>
            <TabsTrigger value="sensitivity">Sensitivity</TabsTrigger>
            <TabsTrigger value="scenarios">Scenarios</TabsTrigger>
          </TabsList>

          <TabsContent value="projection" className="mt-4">
            <div className="h-64 relative">
              <canvas ref={projectionChartRef} className="w-full h-full"></canvas>
            </div>
          </TabsContent>

          <TabsContent value="sensitivity" className="mt-4">
            <div className="h-64 relative">
              <canvas ref={sensitivityChartRef} className="w-full h-full"></canvas>
            </div>
          </TabsContent>

          <TabsContent value="scenarios" className="mt-4">
            <div className="h-64 relative">
              <canvas ref={scenarioChartRef} className="w-full h-full"></canvas>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};
