import { AfterViewInit, Component, EventEmitter, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { QueryNeo4jService } from '../app-services';
import { MatSidenav } from '@angular/material/sidenav';
import { MatCheckbox } from '@angular/material/checkbox';

@Component({
  selector: 'app-unit-analyse-select-menu',
  templateUrl: './unit-analyse-select-menu.component.html',
  styleUrls: ['./unit-analyse-select-menu.component.css']
})
export class UnitAnalyseSelectMenuComponent implements OnChanges, AfterViewInit {
  @Input() which: readonly ("Experiment" | "PreData" | "PostData" | "CPA" | "Process")[] = []
  @ViewChild('drawer') drawer!: MatSidenav;
  @ViewChild('checkbox') checkbox!: MatCheckbox;

  selectedId: string[] = []

  idList!: string[]

  constructor(
    private queryNeo4jService: QueryNeo4jService,
  ) { }
  ngAfterViewInit(): void {
    this.drawer.close()
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.selectedId = []
    this.idList = []
    if (this.checkbox){
      this.checkbox.checked = false
    }
    
    if (this.which[0]) {
      this.drawer.open()
      this.queryNeo4jService.queryOneType(this.which[0]).then((res) => {
        this.idList = JSON.parse(res)
      })
    }
  }


  isSelected(value: string): boolean {
    return this.selectedId.indexOf(value) != -1
  }

  OnDeleteOne(item: string) {
    this.selectedId = this.selectedId.filter((element: string) => element !== item);
  }

  setSelect(value: string) {
    if (this.selectedId.indexOf(value) == -1) {
      if (this.which[0] === 'PreData' || this.which[0] === 'PostData'){
        this.selectedId.push(value)
      } else {
        this.selectedId = [value]
      }
      
    } else{
      this.selectedId = this.selectedId.filter((item: string) => item !== value);
    }
    this.selectedId = [...this.selectedId]
  }

  selectAll(event:any){
    if (event.checked){
      this.selectedId = this.idList
    this.selectedId = [...this.selectedId]
    }else{
      this.selectedId = []
    }
    
  }
}