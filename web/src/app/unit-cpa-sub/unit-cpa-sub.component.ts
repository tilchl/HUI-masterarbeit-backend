import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { QueryNeo4jService } from '../app-services';
import * as Highcharts from 'highcharts';
import HC_more from 'highcharts/highcharts-more';
import HC_accessibility from 'highcharts/modules/accessibility';

@Component({
  selector: 'app-unit-cpa-sub',
  templateUrl: './unit-cpa-sub.component.html',
  styleUrls: ['./unit-cpa-sub.component.css']
})
export class UnitCpaSubComponent implements OnChanges, OnInit {
  @Input() cpa_id!: string
  @Input() sub!: any
  Highcharts: typeof Highcharts = Highcharts;
  curve: { [k: string]: string[] } = {}
  showOrNot: boolean = false
  chartOptions!: Highcharts.Options
  chartOptionsSub!: Highcharts.Options
  showSub: boolean = false

  constructor(
    private queryNeo4jService: QueryNeo4jService,
  ) { }

  ngOnInit(): void {
    HC_more(Highcharts)
    HC_accessibility(Highcharts);
  }

  ngOnChanges() {
    this.curve = {}
    this.showOrNot = false
    this.showSub = false
    if (this.sub.class && this.sub.unique_id) {
      this.queryNeo4jService.queryOneNode(this.sub.class, this.sub.unique_id).then((res: any) => {
        this.curve = JSON.parse(res['Curve'].replace(/'/g, '"'))
        if (this.sub.class === 'FTIR') {
          this.updateFTIR()
        }
        else if (this.sub.class === 'DSC') {
          this.updateDSC()
          this.updateDSCSub()
        }
      })
    }
  }

  updateFTIR() {
    this.chartOptions = {
      chart: {
        zooming: {
          type: 'x'
        }
      },
      title: {
        text: `${this.sub.class} of <u>${this.cpa_id}</u>`
      },
      subtitle: {
        text: `${this.sub.unique_id}`
      },
      xAxis: {
        // categories: this.curve["Wavenumber/cm^-1"].map((numString: string) => {
        //   return `${Number(numString)}`;
        // }),
        reversed: true,
        tickInterval: 250,
        minorTickInterval: 50,
      },
      yAxis: {
        title: {
          text: "Absorbance/A"
        }
      },
      // tooltip: {
      //   valueSuffix: ' (1000 MT)'
      // },
      plotOptions: {
        area: {
          fillOpacity: 0.2
        }
      },
      series: [
        {
          type: 'area',
          data: (this.curve["Absorbance/A"].map((item, index) => [Number(this.curve['Wavenumber/cm^-1'][index]), Number(item)])).reverse(),
          lineWidth: 0.5,
          name: "Wavenumber/cm^-1",
          tooltip: {
            headerFormat: '<span style="color:{series.color}">\u25CF </span><span>{series.name}: <b>{point.x}</b></span><br/>',
            pointFormatter: function () {
              return '<span style="color:white">\u25CF</span> ' + 'Absorbance/A' + ': <b>' + this.y;
            }
          },
          dataGrouping: {
            enabled: false
          }
        }
      ]
    };
    this.showOrNot = true
  }

  updateDSC() {
    this.chartOptions = {
      chart: {
        zooming: {
          type: 'x'
        }
      },
      title: {
        text: `${this.sub.class} of <u>${this.cpa_id}</u>`
      },
      subtitle: {
        text: `${this.sub.unique_id}`
      },
      xAxis: {
        // categories: this.curve["Time/min"]
        //   .map((numString: string) => {
        //     return `${(Number(numString)).toFixed(3)}`;
        //   }),
        tickInterval: 5,
        minorTickInterval: 0.5,
        type: 'linear',
        title: {
          text: "Time/min"
        }
      },
      yAxis: [
        {
          title: {
            text: 'Values'
          },
        }, {
          title: {
            text: "Temp./\u00b0C"
          },
          opposite: true
        }],
      // tooltip: {
      //   valueSuffix: ' (1000 MT)'
      // },
      plotOptions: {
        spline: {
          marker: {
            radius: 4,
            lineColor: '#666666',
            lineWidth: 1
          },
          lineWidth: 4,
        }
      },
      series: [
        {
          type: 'spline',
          data: this.curve["DSC/(mW/mg)"].map((item, index) => [Number(this.curve['Time/min'][index]), Number(item)]),
          name: "DSC/(mW/mg)",
          tooltip: {
            headerFormat: '<span style="color:{series.color}">\u25CF </span><span>Time/min: <b>{point.x}</b></span><br/>',
            pointFormatter: function () {
              return '<span style="color:white">\u25CF</span> ' + "DSC/(mW/mg)" + ': <b>' + this.y;
            }
          },
        },
        {
          type: 'spline',
          data: this.curve["Temp./\u00b0C"].map((item, index) => [Number(this.curve['Time/min'][index]), Number(item)]),
          name: "Temp./\u00b0C",
          tooltip: {
            headerFormat: '<span style="color:{series.color}">\u25CF </span><span>Time/min: <b>{point.x}</b></span><br/>',
            pointFormatter: function () {
              return '<span style="color:white">\u25CF</span> ' + "Temp./\u00b0C" + ': <b>' + this.y;
            }
          },
          yAxis: 1
        },
        {
          type: 'spline',
          data: this.curve["Sensit./(uV/mW)"].map((item, index) => [Number(this.curve['Time/min'][index]), Number(item)]),
          name: "Sensit./(uV/mW)",
          tooltip: {
            headerFormat: '<span style="color:{series.color}">\u25CF </span><span>Time/min: <b>{point.x}</b></span><br/>',
            pointFormatter: function () {
              return '<span style="color:white">\u25CF</span> ' + "Sensit./(uV/mW)" + ': <b>' + this.y;
            }
          },
        },
        {
          type: 'spline',
          data: this.curve["Segment"].map((item, index) => [Number(this.curve['Time/min'][index]), Number(item)]),

          name: "Segment",
          tooltip: {
            headerFormat: '<span style="color:{series.color}">\u25CF </span><span>Time/min: <b>{point.x}</b></span><br/>',
            pointFormatter: function () {
              return '<span style="color:white">\u25CF</span> ' + "Segment" + ': <b>' + this.y;
            }
          },
        },
      ]
    };
    this.showOrNot = true
  }

  updateDSCSub() {
    this.chartOptionsSub = {
      chart: {
        zooming: {
          type: 'x'
        }
      },
      title: {
        text: `${this.sub.class} of <u>${this.cpa_id}</u>`
      },
      subtitle: {
        text: `${this.sub.unique_id}`
      },
      xAxis: {
        labels: {
          format: '{value}\u00b0'
        }
      },
      yAxis: {
        title: {
          text: "DSC/(mW/mg)"
        }
      },
      plotOptions: {
        spline: {
          marker: {
            radius: 4,
            lineColor: '#666666',
            lineWidth: 1
          },
          lineWidth: 4,
        }
      },
      series: [
        {
          type: 'spline',
          data: this.curve["Temp./\u00b0C"].map((item, index) => [Number(item), Number(this.curve['DSC/(mW/mg)'][index])]),
          name: "Temp./\u00b0C",
          tooltip: {
            headerFormat: '<span style="color:{series.color}">\u25CF </span><span>{series.name}: <b>{point.x}</b></span><br/>',
            pointFormatter: function () {
              return '<span style="color: white">\u25CF</span> ' + "DSC/(mW/mg)" + ': <b>' + this.y;
            }
          },
        },
      ]
    };
    this.showSub = true
  }
}
