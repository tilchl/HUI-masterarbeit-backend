import { AfterViewInit, Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { QueryNeo4jService, CalculatorService } from '../app-services';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { MatDialog } from '@angular/material/dialog';
import { UnitEditDatabaseComponent } from '../unit-edit-database/unit-edit-database.component';

@Component({
  selector: 'app-unit-analyse-cell',
  templateUrl: './unit-analyse-cell.component.html',
  styleUrls: ['./unit-analyse-cell.component.css']
})
export class UnitAnalyseCellComponent implements OnChanges, AfterViewInit {
  @Input() staticOrNot!: boolean
  @Input() openSearch!: { which: "Experiment" | "PreData" | "PostData" | "CPA" | "Process", selectedId: string[] }
  @Output() deleteOne: EventEmitter<string> = new EventEmitter<string>()
  callBacks: any[] = []
  shortTimeMemory: any[] = []
  dataSource = new MatTableDataSource([])
  showTable: boolean = false
  itemShow: { [key: string]: string[] } = {
    Viability: ["Viability_(%)", "Total_cells_/_ml_(x_10^6)", "Total_viable_cells_/_ml_(x_10^6)"],
    Morphology: ["Average_diameter_(microns)", "Average_circularity", "Cell_type"],
  }
  topItems: string[] = ["Sample_ID", "RunDate", "Machine"]
  tableHeader = ['Sample_ID', ...this.itemShow['Viability'], ...this.itemShow['Morphology']]
  selected = 0
  seeMore: string[] = []
  constructor(
    private queryNeo4jService: QueryNeo4jService,
    private calculatorService: CalculatorService,
    public dialog: MatDialog,
  ) { }

  result: any = { "Sample_ID": 'CONCLUSION' }

  searchOne(ID: readonly string[], data_type: "Experiment" | "PreData" | "PostData" | "CPA" | "Process") {
    ID.forEach((element) => {
      this.queryNeo4jService.queryOneNode(data_type, element).then((res) => {
        this.shortTimeMemory.push(res)
        this.shortTimeMemory = [...this.shortTimeMemory]

        if (ID.length === this.shortTimeMemory.length && this.shortTimeMemory.length !== 0) {
          this.shortTimeMemory.sort((a, b) => {
            return a.Sample_ID.localeCompare(b.Sample_ID);
          });
          this.callBacks = this.shortTimeMemory
          this.tableHeader.forEach(item => {
            if (['Sample_ID', 'Cell_type'].indexOf(item) === -1) {
              this.calculatorService.getMeanAndVariance(this.callBacks.map(obj => obj[item])).then((res) => {
                this.result[item] = res
                this.result = { ...this.result }
                this.dataSource = new MatTableDataSource(this.makeSource())
                this.ngAfterViewInit()
              })
            }
          })
        }
      })
    })

  }
  makeSource(): any {
    this.showTable = true
    return this.callBacks.concat(this.result)
  }
  ngOnChanges(changes: SimpleChanges) {
    if (changes['openSearch']) {
      this.callBacks = []
      this.shortTimeMemory = []
      this.showTable = false
      this.dataSource = new MatTableDataSource([])

      if (this.openSearch['selectedId'].length !== 0) {
        this.searchOne(this.openSearch['selectedId'], this.openSearch['which'])
      }
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

  clickedRow(row: any) {
    if (this.callBacks.indexOf(row) != -1) {
      this.selected = this.callBacks.indexOf(row)
    }
  }
  isString(input: any): boolean {
    return typeof input === 'string';
  }

  @ViewChild(MatSort) sort!: MatSort;

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }



  // /** Announce the change in sort state for assistive technology. */
  // announceSortChange(sortState: Sort) {
  //   console.log(sortState)
  //   if (sortState.direction) {
  //     this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
  //   } else {
  //     this._liveAnnouncer.announce('Sorting cleared');
  //   }
  // }

  sortData(sort: Sort): void {
    const data: any = this.dataSource.data.slice();
    if (!sort.active || sort.direction === '') {
      this.dataSource.data = data;
      return;
    }

    this.dataSource.data = data.sort((a: any, b: any) => {
      if (a['Sample_ID'] == 'CONCLUSION' || b['Sample_ID'] == 'CONCLUSION') {
        return 1
      }
      else {
        let isAsc: boolean = sort.direction === 'asc';
        return this.compare(a[sort.active], b[sort.active], isAsc,);
      }
    }
    );
    this.dataSource = new MatTableDataSource(this.dataSource.data);
  }
  compare(a: any, b: any, isAsc: boolean): number {
    if (a < b) {
      return -1 * (isAsc ? 1 : -1);
    } else if (a > b) {
      return 1 * (isAsc ? 1 : -1);
    } else {
      return 0 * (isAsc ? 1 : -1);
    }
  }
  openDialogGraph(callBack: any): void {
    let dialogRef = this.dialog.open(UnitEditDatabaseComponent, {
      width: '70%',
      height: '70%',
    })
    let instance = dialogRef.componentInstance
    instance['callBack'] = callBack
    instance['type'] = this.openSearch['which']
  }

  seeMoreAttr() {
    this.seeMore.push('')
  }
}
