import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CalculatorService } from '../app-services';
import * as Highcharts from 'highcharts';
import HC_more from 'highcharts/highcharts-more';
import HC_accessibility from 'highcharts/modules/accessibility';
import HC_drilldown from 'highcharts/modules/drilldown';
import HC_exportData from 'highcharts/modules/export-data';
import HC_exporting from 'highcharts/modules/exporting';

@Component({
  selector: 'app-unit-analyse-exp-graph',
  templateUrl: './unit-analyse-exp-graph.component.html',
  styleUrls: ['./unit-analyse-exp-graph.component.css'],
})
export class UnitAnalyseExpGraphComponent implements OnChanges {
  hash: { [k: string]: string } = {
    viabilityppn: 'norm. rel. viability',
    durchmetterppn: 'norm. rel. diameter',
    recoveried_cellsppn: 'norm. recovery rate',
    rundheitppn: 'norm. rel. circularity',
    viabilitypp: 'rel. viability',
    durchmetterpp: 'rel. diameter',
    recoveried_cellspp: 'recovery rate',
    rundheitpp: 'rel. circularity'
  }

  @Input() sortedResultData!: { [key: string]: { [k: string]: [string, string][] } }
  @Input() which!: string
  @Input() classColors: any
  dataToShow: any
  chartOptions!: Highcharts.Options
  Highcharts: typeof Highcharts = Highcharts;
  show: boolean = false

  chartOptionsBoxplot!: Highcharts.Options
  showBoxplot: boolean = false

  tableData: any = {}
  showTable: boolean = false
  tableHeader: string[] = ["group1", "group2", "meandiff", "p-adj", "lower", "upper", "reject"]
  tableHeaderSumm: string[] = ['factor', "mean", "variance", "SD", 'SE', "CI 95%", 'low', 'q1', 'median', 'q3', 'high', 'outliers', 'expand']
  tableSummery: any = []
  showSummery: boolean = false
  constructor(
    private calculatorService: CalculatorService,
  ) {

  }

  ngOnInit(): void {
    HC_more(Highcharts)
    HC_accessibility(Highcharts);
    HC_drilldown(Highcharts);
    HC_exportData(Highcharts);
    HC_exporting(Highcharts);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['which']['currentValue']) {
      this.buildColumn()
    }
  }

  buildColumn() {
    this.show = false
    this.showSummery = false
    this.calculatorService.buildColumn(this.getDataToShow(this.which)).then((res: any) => {
      this.dataToShow = res
      this.anovaTest()
      this.getTableDataSummery()
    })
  }

  getDataToShow(which: string | null): { [key: string]: [string, string][] } {
    if (which) {
      let out: { [key: string]: [string, string][] } = {}
      this.getObjectKeys(this.sortedResultData).forEach((faktor: string) => {
        out[faktor] = this.sortedResultData[faktor][which]
      })
      return out
    } else {
      return {}
    }
  }

  getObjectKeys(obj: any): string[] {
    if (Object.keys(obj).length === 0) {
      return []
    }
    else {
      return Object.keys(obj);
    }
  }

  anovaTest() {
    this.tableData = {}
    this.showTable = false
    this.tableSummery = []
    this.calculatorService.anovaTest(this.getDataToShow(this.which)).then((res: any) => {
      this.tableData = res
      this.updateChartOptions()
      this.show = true
      this.showTable = true
    })
  }

  updateChartOptions() {
    let self = this
    this.chartOptions = {
      title: {
        align: 'left',
        text: this.hash[this.which]
      },
      subtitle: {
        align: 'left',
        text: 'Click the columns to view trial data.'
      },
      xAxis: {
        type: 'category'
      },
      yAxis: [{
        title: {
          text: '%'
        }
      }],
      legend: {
        enabled: false
      },
      plotOptions: {
        column: {
          pointPadding: 0.2,
          borderWidth: 0,
        }
      },
      series: [
        {
          name: this.hash[this.which],
          type: 'column',
          colorByPoint: true,
          data: this.getObjectKeys(this.dataToShow).map(faktor_id => {
            return { y: parseFloat(this.dataToShow[faktor_id]['mean']), drilldown: faktor_id, name: faktor_id }
          }),
          tooltip: {
            pointFormatter: function () {
              return '<span style="color:' + this.color + '">\u25CF</span> mean = <b>' + this.y
                + '</b><br/><span style="color:' + this.color + '">\u25CF</span> n = ' + self.dataToShow[this.name]['n']
                + '<br/><span style="color:' + this.color + '">\u25CF</span> CI 95% = ' + JSON.stringify(self.dataToShow[this.name]['CI 95%'])
            }
          },
        },
        {
          name: 'CI 95%',
          type: 'errorbar',
          data: this.getObjectKeys(this.dataToShow).map(faktor_id => {
            return {
              low: parseFloat(this.dataToShow[faktor_id]['CI 95%'][0]),
              high: parseFloat(this.dataToShow[faktor_id]['CI 95%'][1]),
              drilldown: faktor_id + 'errorbar'
            }
          }),
          dataLabels: {
            enabled: true,
            formatter: function () {
              if (this.point.high === this.y) {
                const index: number = checkType(this.point.category)
                this.point.name = self.getObjectKeys(self.dataToShow)[index]
                return self.tableData['Tukey Group'][self.getObjectKeys(self.dataToShow)[index]];
              }
              return null;
            },
          },
          tooltip: {
            pointFormatter: function () {
              return ''
            }
          },
        }
      ],
      drilldown: {
        allowPointDrilldown: false,
        series: [],
        activeAxisLabelStyle: {
          position: 'end'
        }
      },
      exporting: {
        buttons: {
          contextButton: {
            menuItems: [
              'viewFullscreen', 'separator', 'downloadPNG',
              'downloadSVG', 'downloadPDF'
            ]
          },
        },
        enabled: true,
      },
      navigation: {
        buttonOptions: {
          align: 'right',
          verticalAlign: 'top',
          y: 0
        }
      },
    }

    this.getObjectKeys(this.dataToShow).forEach(faktor_id => {

      let out: { [k: string]: any } = {}
      this.getDataToShow(this.which)[faktor_id].forEach((item: [string, string]) => {
        if (!out[item[1]]) {
          out[item[1]] = [item]
        } else {
          out[item[1]].push(item)
        }
      })
      this.calculatorService.buildColumn(out).then((res: any) => {
        const drillData: any = this.getObjectKeys(res).map((versuch_id: string) => {
          return { name: versuch_id, y: parseFloat(res[versuch_id]['mean']), color: this.classColors[versuch_id] }
        })
        this.chartOptions.drilldown?.series?.push({
          type: 'column', id: faktor_id, data: drillData, name: faktor_id,
          // dataLabels: {
          //   enabled: true,
          //   format: '{point.y:.4f}',
          //   position:'right'
          // }, 
          tooltip: {
            pointFormatter: function () {
              return '<span style="color:' + this.color + '">\u25CF</span> mean = <b>' + this.y
                + '</b><br/><span style="color:' + this.color + '">\u25CF</span> n = ' + res[this.name]['n']
                + '<br/><span style="color:' + this.color + '">\u25CF</span> CI 95% = ' + JSON.stringify(res[this.name]['CI 95%'])
            }
          },
        })

        this.chartOptions.drilldown?.series?.push({
          type: 'errorbar', id: faktor_id + 'errorbar', data: this.getObjectKeys(res).map((versuch_id: string) => {
            return { low: parseFloat(res[versuch_id]['CI 95%'][0]), high: parseFloat(res[versuch_id]['CI 95%'][1]), name: versuch_id }
          }), name: 'CI 95%', tooltip: {
            pointFormatter: function () {
              return ''
            }
          },
        })
      })
    })
  }

  updateChartOptionsBoxplot() {
    const self = this
    this.chartOptionsBoxplot = {
      title: {
        align: 'left',
        text: this.hash[this.which]
      },
      subtitle: {
        align: 'left',
        text: 'Click the columns to view trial data.'
      },
      xAxis: {
        type: 'category'
      },
      yAxis: [{
        title: {
          text: '%'
        }
      }],
      legend: {
        enabled: false
      },
      plotOptions: {
        column: {
          pointPadding: 0.2,
          borderWidth: 0,
        }
      },
      series: [
        {
          name: this.hash[this.which],
          type: 'boxplot',
          colorByPoint: true,
          data: this.getObjectKeys(this.dataToShow).map(faktor_id => {
            return { low: parseFloat(this.dataToShow[faktor_id]['low']), q1: parseFloat(this.dataToShow[faktor_id]['q1']), median: parseFloat(this.dataToShow[faktor_id]['median']), q3: parseFloat(this.dataToShow[faktor_id]['q3']), high: parseFloat(this.dataToShow[faktor_id]['high']), drilldown: faktor_id, name: faktor_id }
          }),
          tooltip: {
            pointFormatter: function () {
              return '<span style="color:' + this.color + '">\u25CF</span> mean = <b>' + self.dataToShow[this.name]['mean']
                + '</b><br/><span style="color:' + this.color + '">\u25CF</span> high = ' + this.options.high
                + '<br/><span style="color:' + this.color + '">\u25CF</span> q3 = ' + this.options.q3
                + '<br/><span style="color:' + this.color + '">\u25CF</span> median = ' + this.options.median
                + '<br/><span style="color:' + this.color + '">\u25CF</span> q1 = ' + this.options.q1
                + '<br/><span style="color:' + this.color + '">\u25CF</span> low = ' + this.options.low
            }
          },
        },
        {
          name: 'Outliers',
          color: 'red',
          type: 'scatter',
          data: this.getOutliers(),
          marker: {
            fillColor: 'white',
            lineWidth: 1,
            lineColor: 'red'
          },
          tooltip: {
            pointFormat: `{point.name}: {point.y}`
          }
        },
        {
          name: 'mean',
          type: 'scatter',
          data: this.getObjectKeys(this.dataToShow).map(faktor_id => {
            return { drilldown: faktor_id + 'out', name: faktor_id, y: parseFloat(this.dataToShow[faktor_id]['mean']) }
          }),
          marker: {
            fillColor: 'white',
            lineWidth: 1,
            lineColor: 'green'
          },
          tooltip: {
            pointFormat: `{point.name}: {point.y}`
          }
        }
      ],
      drilldown: {
        allowPointDrilldown: false,
        series: [],
        activeAxisLabelStyle: {
          position: 'end'
        }
      },

      exporting: {
        buttons: {
          contextButton: {
            menuItems: [
              'viewFullscreen', 'separator', 'downloadPNG',
              'downloadSVG', 'downloadPDF'
            ]
          },
        },
        enabled: true,
      },
      navigation: {
        buttonOptions: {
          align: 'right',
          verticalAlign: 'top',
          y: 0
        }
      },
    }

    this.getObjectKeys(this.dataToShow).forEach(faktor_id => {
      this.getDrillDownBoxplot(faktor_id)
    })

  }

  getOutliers(): any[] {
    let outliers: any[] = []
    this.getObjectKeys(this.dataToShow).forEach((faktor_id: string, index: number) => {
      if (this.dataToShow[faktor_id]['outliers'].length != 0) {
        outliers = outliers.concat(this.dataToShow[faktor_id]['outliers'].map((item: number) => {
          return { name: faktor_id, y: item }
        }))
      }
    })
    return outliers
  }

  setGreen(value: any) {
    return value === true
  }

  getDrillDownBoxplot(faktor_id: string) {
    let out: { [k: string]: any } = {}
    this.getDataToShow(this.which)[faktor_id].forEach((item: [string, string]) => {
      if (!out[item[1]]) {
        out[item[1]] = [item]
      } else {
        out[item[1]].push(item)
      }
    })
    this.calculatorService.buildColumn(out).then((res: any) => {
      const drillData: { low: number, q1: number, median: number, q3: number, high: number, name: string, color: any }[] = []
      this.getObjectKeys(res).forEach((versuch_id: string) => {
        this.tableSummery.forEach((item: any) => {
          if (item['factor'] === faktor_id) {
            if (!item['child']) {
              item['child'] = []
            }
            item['child'].push({ factor: versuch_id, ...res[versuch_id] })
            return false
          }
          return true
        })
        drillData.push({ low: parseFloat(res[versuch_id]['low']), q1: parseFloat(res[versuch_id]['q1']), median: parseFloat(res[versuch_id]['median']), q3: parseFloat(res[versuch_id]['q3']), high: parseFloat(res[versuch_id]['high']), name: versuch_id, color: darkenColor(this.classColors[versuch_id]) })
      })
      this.chartOptionsBoxplot.drilldown?.series?.push({
        type: 'boxplot', id: faktor_id, data: drillData, name: faktor_id,
        tooltip: {
          pointFormatter: function () {
            return '<span style="color:' + this.color + '">\u25CF</span> mean = <b>' + res[this.name]['mean']
              + '</b><br/><span style="color:' + this.color + '">\u25CF</span> high = ' + this.options.high
              + '<br/><span style="color:' + this.color + '">\u25CF</span> q3 = ' + this.options.q3
              + '<br/><span style="color:' + this.color + '">\u25CF</span> median = ' + this.options.median
              + '<br/><span style="color:' + this.color + '">\u25CF</span> q1 = ' + this.options.q1
              + '<br/><span style="color:' + this.color + '">\u25CF</span> low = ' + this.options.low
          }
        },
      })

      let outliers: any[] = []
      this.getObjectKeys(res).forEach((versuch_id: string, index: number) => {
        if (res[versuch_id]['outliers'].length != 0) {
          outliers = outliers.concat(res[versuch_id]['outliers'].map((item: number) => {
            return { name: versuch_id, y: item }
          }))
        }
      })
      this.chartOptionsBoxplot.drilldown?.series?.push({
        type: 'scatter', id: faktor_id + 'out', data: outliers, name: 'Outliers', marker: {
          fillColor: 'white',
          lineWidth: 1,
          lineColor: 'red'
        },
        tooltip: {
          pointFormat: `{point.name}: {point.y}`
        }
      })

    })


  }

  getTableDataSummery() {
    this.showBoxplot = false
    this.tableSummery = this.getObjectKeys(this.dataToShow).map((item: string) => {
      return { factor: item, ...this.dataToShow[item], expand: false }
    })
    this.updateChartOptionsBoxplot()
    this.showBoxplot = true
    this.showSummery = true
  }

  expand(faktor_id: string, child: any) {
    if (child) {
      this.tableSummery.forEach((item: any, index: number) => {
        if (item['factor'] === faktor_id) {
          if (item['expand']) {
            this.tableSummery.splice(index + 1, item['child'].length)
          }
          else {
            this.tableSummery.splice(index + 1, 0, ...item['child'])
          }
          item['expand'] = !item['expand']
          return false
        }
        return true
      })
      this.tableSummery = [...this.tableSummery]
    }

  }
}


function checkType(value: any): number {
  if (typeof value === 'string') {
    return parseInt(value)
  } else if (typeof value === 'number') {
    return value
  } else {
    return 0
  }
}

function darkenColor(color: string, factor: number = 50) {
  const r = parseInt(color.slice(1, 3), 16);
  const g = parseInt(color.slice(3, 5), 16);
  const b = parseInt(color.slice(5, 7), 16);

  const newR = Math.max(0, r - factor);
  const newG = Math.max(0, g - factor);
  const newB = Math.max(0, b - factor);

  const newColor = `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;

  return newColor;
}
