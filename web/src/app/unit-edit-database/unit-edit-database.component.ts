import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { QueryNeo4jService } from '../app-services';
import { MatSelect } from '@angular/material/select';
import { String, cloneDeep, indexOf } from 'lodash';
import { defaultVersuche, defaultProbe, defaultCpaData } from '../app-config';

@Component({
  selector: 'app-unit-edit-database',
  templateUrl: './unit-edit-database.component.html',
  styleUrls: ['./unit-edit-database.component.css']
})
export class UnitEditDatabaseComponent implements AfterViewInit {
  callBack!: any
  type!: string
  error: { [key: string]: string } = { fileName: '', cpaIndex: '' }

  currentFileName: string = ''
  defaultCpaData = cloneDeep(defaultCpaData)
  currentCpaItemType: string = ''
  undoDisabled: boolean = false

  //only for cpa
  currentCpaIndex: string = ''
  oldSubName: { [key: string]: string } = {}
  currentSubName: { [key: string]: string } = {}
  statusSubName: { [key: string]: string } = {}
  currentFfactor: { [key: string]: string } = {}
  statusFfactor: { [key: string]: string } = {}
  pppcDataControler: { [key: string]: { [key: string]: any } } = {}
  pppcDataMemory: { [key: string]: { [key: string]: any } } = {}
  addControler: { [key: string]: any } = {}
  addControlerProbe: { [key: string]: any } = {}

  translate: { [k: string]: ("PreData" | "PostData" | "CPA" | "Process") } = {
    "PreData ID": 'PreData',
    "PostData ID": 'PostData',
    "CPA ID": 'CPA',
    "Process ID": 'Process'
  }

  idList: { [key: string]: string[] } = {}

  constructor(
    private queryNeo4jService: QueryNeo4jService
  ) {
    // this.currentFileName = this.callBack['experiment']['Experiment_ID']
  }

  response: { addition: any, deletion: any, changeAttr: any, changeName: any } = { addition: [], deletion: { fatherNodes: [], childrenNodes: [], nodeAttributes: [] }, changeAttr: [], changeName:[] }

  init(){
    this.error = { fileName: '', cpaIndex: '' }
    this.currentFileName = ''
    this.defaultCpaData = cloneDeep(defaultCpaData)
    this.currentCpaItemType = ''
    this.currentCpaIndex = ''
    this.undoDisabled = false
    this.oldSubName = {}
    this.currentSubName = {}
    this.currentFfactor = {}
    this.statusSubName = {}
    this.statusFfactor = {}
    this.pppcDataControler = {}
    this.pppcDataMemory = {}
    this.addControler = {}
    this.addControlerProbe = {}
    this.key = ''
    this.value = ''
    this.createAttrError = ''
    this.resultStatus = false
    this.todoSQL = { addition: [], deletion: {}, changeAttr: [], changeName:[] }
    this.deletedItems = { fatherNodes: [], childrenNodes: [], nodeAttributes: [] }
    this.defaultCpaData = cloneDeep(defaultCpaData)
    this.response = { addition: [], deletion: { fatherNodes: [], childrenNodes: [], nodeAttributes: [] }, changeAttr: [], changeName:[] }
  }
  ngAfterViewInit() {
    setTimeout(() => {
      this.init()
      if (this.type === 'Experiment') {
        this.currentFileName = this.callBack['experiment']['Experiment_ID']
        if (this.callBack['child'][0]['probes'].length){
            this.callBack['child'].forEach((item: any) => {
            this.oldSubName[item['versuch']['Unique_ID']] = item['versuch']['Versuch_ID']
            this.currentSubName[item['versuch']['Unique_ID']] = item['versuch']['Versuch_ID']
            this.currentFfactor[item['versuch']['Unique_ID']] = item['versuch']['F_factor']
            this.statusSubName[item['versuch']['Unique_ID']] = 'none'
            this.statusFfactor[item['versuch']['Unique_ID']] = 'none'
            item['probes'].forEach((sub: any) => {
              this.oldSubName[sub['Unique_ID']] = sub['Sample_ID']
              this.currentSubName[sub['Unique_ID']] = sub['Sample_ID']
              this.statusSubName[sub['Unique_ID']] = 'none'
              this.pppcDataControler[sub['Unique_ID']] = { PreData_ID: sub['PreData_ID'], PostData_ID: sub['PostData_ID'], Process_ID: sub['Process_ID'], CPA_ID: sub['CPA_ID'] }
            })
          })
          this.pppcDataMemory = cloneDeep(this.pppcDataControler)
        }
      }
      else if (this.type === 'CPA') {
        this.currentCpaIndex = this.callBack['cpa']['CPA_ID']
        if (this.callBack['child'][0]['unique_id']){
            this.callBack['child'].forEach((item: any) => {
            this.oldSubName[`${item['class']}*-*${item['unique_id']}`] = item['unique_id']
            this.currentSubName[`${item['class']}*-*${item['unique_id']}`] = item['unique_id']
            this.statusSubName[`${item['class']}*-*${item['unique_id']}`] = 'none'
            this.pppcDataControler[`${item['class']}*-*${item['unique_id']}`] = cloneDeep(item['properties'])
          })
          this.pppcDataMemory = cloneDeep(this.pppcDataControler)
        }
      }
      else if (this.type === 'Process') {
        this.currentFileName = this.callBack['Process_ID']
        this.pppcDataControler = cloneDeep(this.callBack)
      }
      else if (this.type === 'PreData' || this.type === 'PostData') {
        this.currentFileName = this.callBack['Sample_ID']
        this.pppcDataControler = cloneDeep(this.callBack)
      }
      else {

      }
    }, 0);
  }

  helpCheck(type: string) {
    if (type === 'Experiment') {
      return this.currentFileName === this.callBack['experiment']['Experiment_ID']
    }
    else if (type === 'CPA') {
      return this.currentCpaIndex === this.callBack['cpa']['CPA_ID']
    }
    else if (type === 'Process') {
      return this.currentFileName === this.callBack['Process_ID']
    }
    else {
      return this.currentFileName === this.callBack['Sample_ID']
    }
  }

  checkTheName(type: string, oldName: string, currentName: string) {
    if (currentName === '') {
      this.statusSubName[`${type}*-*${oldName}`] = 'type2'
    }
    else {
      if (this.oldSubName[`${type}*-*${oldName}`] === this.currentSubName[`${type}*-*${oldName}`] && this.oldSubName[`${type}*-*${oldName}`]) {
        this.statusSubName[`${type}*-*${oldName}`] = 'none'
      }
      else {
        this.queryNeo4jService.duplicateCheck(type, currentName).then((res) => {
          //if already has, be true\
          if (res) {
            this.statusSubName[`${type}*-*${oldName}`] = 'type3'
          } else {
            this.statusSubName[`${type}*-*${oldName}`] = 'none'
          }
        })
      }
    }
  }

  checkFfactor(versuch_unique:string, oldF:string, currentF: string) {
    if (!currentF){
      this.statusFfactor[versuch_unique] = 'type2'
    }
    else if (!Number(currentF)){
      this.statusFfactor[versuch_unique] = 'type3'
    }
    else {
      if (Number(currentF) === Number(oldF)){
        this.statusFfactor[versuch_unique] = 'none'
      }
      else{
        this.statusFfactor[versuch_unique] = 'change'
      }
    }
  }
  isNumber(value: any): boolean {
    return !Number(value)
  }

  checkTheVersuch(versuchOrProbe: 'Versuch' | 'Probe', unique_id: string, currentName: string) {
    if (currentName === '') {
      this.statusSubName[unique_id] = 'type2'
    }
    else {
      let allId: string[] = []
      if (versuchOrProbe === 'Versuch') {
        this.callBack['child'].forEach((versuch: any) => {
          allId.push(this.currentSubName[versuch['versuch']['Unique_ID']])
        })
        this.getObjectKeys(this.addControler).forEach((nk) => {
          allId.push(this.addControler[nk]['Versuche ID'])
        })
      }
      else {
        this.callBack['child'].forEach((versuch: any) => {
          if (versuch['versuch']['Unique_ID'] == `${unique_id.split('*-*')[0]}*-*${unique_id.split('*-*')[1]}`) {
            versuch['probes'].forEach((sub: any) => {
              allId.push(this.currentSubName[sub['Unique_ID']])
            })
          }
        })
        this.getObjectKeys(this.addControler).forEach((newVersuch: string) => {
          if (newVersuch == unique_id.split('*-*')[0]) {
            this.getObjectKeys(this.addControler[newVersuch]).forEach((probeKey: string) => {
              if (probeKey != 'Versuche ID') {
                allId.push(this.addControler[newVersuch][probeKey]['Sample ID'])
              }
            })
          }
        })
        this.getObjectKeys(this.addControlerProbe).forEach((toVersuch: string) => {
          if (`${unique_id.split('*-*')[0]}*-*${unique_id.split('*-*')[1]}` == toVersuch) {
            (this.addControlerProbe[toVersuch]).forEach((probe: any) => {
              allId.push(probe['Sample ID'])
            })
          }
        })
      }
      if (allId.filter(item => item === currentName).length != 1) {
        this.statusSubName[unique_id] = 'type3'
      }
      else {
        this.statusSubName[unique_id] = 'none'
      }
    }
  }


  search(data_type: string) {
    data_type = data_type.replace('_', ' ')
    this.queryNeo4jService.queryOneType(this.translate[data_type]).then((res) => {
      this.idList[data_type] = JSON.parse(res)
      this.idList = { ...this.idList }
    })

  }


  getObjectKeys(obj: any): string[] {
    if (Object.keys(obj).length === 0) {
      return []
    }
    else {
      return Object.keys(obj);
    }
  }

  parseArray(input: any): boolean {
    try {
      if (Array.isArray(input)) {
        return true;
      }
      return false;
    } catch (error) {
      return false;
    }
  }

  emm(input: string) {
    return input + '_ID'
  }

  rename(type: string, orignalName: string, currentName: string) {

  }

  checkFileName(type: string) {
    if (this.currentFileName.includes('/') || this.currentFileName.includes('\\')) {
      this.error['fileName'] = 'type1'
    } else if (this.currentFileName == '') {
      this.error['fileName'] = 'type2'
    } else {
      if (!this.helpCheck(type)) {
        this.queryNeo4jService.duplicateCheck(type, this.currentFileName).then((res) => {
          if (res) {
            this.error['fileName'] = 'type3'
          } else {
            this.error['fileName'] = 'none'
          }
        })
      }
      else {
        this.error['fileName'] = 'none'
      }
    }
  }

  checkCpaIndex() {
    if (this.currentCpaIndex.includes('/') || this.currentCpaIndex.includes('\\') || this.currentCpaIndex.includes('.')) {
      this.error['cpaIndex'] = 'type1'
    } else if (this.currentCpaIndex == '') {
      this.error['cpaIndex'] = 'type2'
    } else {

      if (!this.helpCheck(this.type)) {
        this.queryNeo4jService.duplicateCheck('CPA', this.currentCpaIndex).then((res) => {
          if (res) {
            this.error['cpaIndex'] = 'type3'
          } else {
            this.error['cpaIndex'] = 'none'
          }
        })
      }
      else {
        this.error['cpaIndex'] = 'none'
      }
    }
  }

  undo() {
    this.error = { fileName: '', cpaIndex: '' }
    this.idList = {}
    this.ngAfterViewInit()
  }

  arraysAreEqual(arr1: any, arr2: any): boolean {
    if (arr1.length !== arr2.length) {
      return false;
    }

    for (let i = 0; i < arr1.length; i++) {
      if (arr1[i] !== arr2[i]) {
        return false;
      }
    }

    return true;
  }

  add(location: string, info: 'Versuche' | 'Attr' | 'Probe' | 'ProbeAtNew' | string) {
    if (info === 'Versuche') {
      this.addControler[`versuch ${this.callBack['child'].length + this.getObjectKeys(this.addControler).length + 1}`] = cloneDeep(defaultVersuche)
      this.statusSubName[`versuch ${this.callBack['child'].length + this.getObjectKeys(this.addControler).length}`] = 'none'
    }
    else if (info === 'Attr') {

    }
    else if (info === 'Probe') {
      if (!this.addControlerProbe[`${location}`]) {
        this.addControlerProbe[`${location}`] = []
      }
      this.addControlerProbe[`${location}`].push(cloneDeep(defaultProbe))
    }
    else if (info === 'ProbeAtNew') {
      this.addControler[location][`Probe ${this.getObjectKeys(this.addControler[location]).length - 1}`] = cloneDeep(defaultProbe)
    }
    else {
      if (info) {
        if (defaultCpaData[info]) {
          this.addControler[info] = cloneDeep(defaultCpaData[info])
        }
        else {
          this.addControler[info] = {}
        }
      }

    }
    this.currentCpaItemType = ''
  }

  getItemCpaList() {
    let list: string[] = []
    this.callBack['child'].forEach((item: any) => {
      list.push(item['class'])
    })
    return this.getObjectKeys(this.addControler).concat(list)
  }
  key: string = ''
  value: string = ''
  createAttrError: string = ''
  addAttributes(body: any, key: string, value: string) {
    if (key == '' || value == '') {
      this.createAttrError = 'type2'
    }
    else {
      if (this.getObjectKeys(body).indexOf(key) != -1) {
        this.createAttrError = 'type3'
      }
      else {
        this.createAttrError = ''
        body[key] = value
        this.key = ''
        this.value = ''
      }
    }
  }
  deletedItems: { fatherNodes: any[], childrenNodes: any[], nodeAttributes: any[] } = { fatherNodes: [], childrenNodes: [], nodeAttributes: [] }
  delete(type: 'fatherNodes' | 'childrenNodes' | 'nodeAttributes', key: any) {
    if (key.attributeKey) {
      if (this.deletedItems[type].findIndex(item => item.attributeKey === key.attributeKey)== -1){
        this.deletedItems[type].push(key)
      }
    }
    else {
        if (this.deletedItems[type].findIndex(item => item.Unique_ID === key.Unique_ID)== -1){
        this.deletedItems[type].push(key)
      }
    }
    
  }

  deleteGenerierted(body: any, key: string | number) {
    if (typeof key === 'string') {
      delete body[key]
    } else if (typeof key === 'number') {
      body.splice(key, 1)
    }
  }

  todoSQL: { addition: any, deletion: any, changeAttr: any, changeName: any } = { addition: [], deletion: {}, changeAttr: [], changeName:[] }
  resultStatus:boolean = false
  generateCommit() {
    this.todoSQL = { addition: [], deletion: {}, changeAttr: [], changeName:[] }
    if (this.type == 'Experiment') {
      this.getObjectKeys(this.addControler).forEach((key: string) => {
        this.todoSQL.addition.push({ class: 'Versuch', father: { class: 'Experiment', Unique_ID: this.callBack['experiment']['Experiment_ID'] }, info: this.addControler[key] })
      })
      this.getObjectKeys(this.addControlerProbe).forEach((key: string) => {
        this.addControlerProbe[key].forEach((probe: any) => {
          this.todoSQL.addition.push({ class: 'Probe', father: { class: 'Versuch', Unique_ID: key }, info: probe })
        })
      })
      this.getObjectKeys(this.pppcDataControler).forEach((key: string) => {
        this.getObjectKeys(this.pppcDataControler[key]).forEach((item: string) => {
          if (!this.arraysAreEqual(this.pppcDataControler[key][item], this.pppcDataMemory[key][item])) {
            this.todoSQL.changeAttr.push({ class: 'Probe', attrKey: item, unique_id: key, currentValue: this.pppcDataControler[key][item] })
          }
        })
      })
      this.getObjectKeys(this.statusFfactor).forEach((key: string) => {
        if (this.statusFfactor[key] === 'change'){
          this.todoSQL.changeAttr.push({ class: 'Versuch', attrKey: 'F_factor', unique_id: key, currentValue: this.currentFfactor[key] })
        }
      })
      this.getObjectKeys(this.currentSubName).forEach((key: string) => {
        const idficationArray: string[] = key.split('*-*')
        let className: string = ''
        if (idficationArray.length === 2) {
          className = 'Versuch'
          if (this.currentSubName[key] != idficationArray[idficationArray.length - 1]) {
            this.todoSQL.changeName.unshift({ class: className, unique_id: key, currentName: this.currentSubName[key] })
          }
        }
        else {
          className = 'Probe'
          if (this.currentSubName[key] != idficationArray[idficationArray.length - 1]) {
            this.todoSQL.changeName.push({ class: className, unique_id: key, currentName: this.currentSubName[key] })
          }
        }
      })
      if (this.currentFileName != this.callBack['experiment']['Experiment_ID']) {
        this.todoSQL.changeName.push({ class: 'Experiment', unique_id: this.callBack['experiment']['Experiment_ID'], currentName: this.currentFileName })
      }
      this.todoSQL.deletion = this.deletedItems
    }
    else if (this.type == 'CPA') {
      this.getObjectKeys(this.pppcDataControler).forEach((key: string) => {
        this.getObjectKeys(this.pppcDataControler[key]).forEach((item: string) => {
          if (this.getObjectKeys(this.pppcDataMemory[key]).indexOf(item) == -1) {
            this.todoSQL.addition.push({ class: key.split('*-*')[0], unique_id: key.split('*-*')[1], attrKey: item, attrValue: this.pppcDataControler[key][item] })
          }
        })
      })
      this.getObjectKeys(this.addControler).forEach((key: string) => {
        this.todoSQL.addition.push({ class: key, info: this.addControler[key], father: { class: 'CPA', Unique_ID: this.callBack['cpa']['CPA_ID'] } })
      })
      this.getObjectKeys(this.pppcDataMemory).forEach((key: string) => {
        this.getObjectKeys(this.pppcDataMemory[key]).forEach((item: string) => {
          if (!this.arraysAreEqual(this.pppcDataControler[key][item], this.pppcDataMemory[key][item])) {
            this.todoSQL.changeAttr.push({ class: key.split('*-*')[0], unique_id: key.split('*-*')[1], attrKey: item, currentValue: this.pppcDataControler[key][item] })
          }
        })
      })
      this.getObjectKeys(this.currentSubName).forEach((key: string) => {
        const idficationArray: string[] = key.split('*-*')
        if (this.currentSubName[key] != idficationArray[idficationArray.length - 1]) {
          this.todoSQL.changeName.push({ class: idficationArray[idficationArray.length - 2], unique_id: idficationArray[idficationArray.length - 1], currentName: this.currentSubName[key] })
        }
      })
      if (this.currentCpaIndex != this.callBack['cpa']['CPA_ID']) {
        this.todoSQL.changeName.push({ class: 'CPA', unique_id: this.callBack['cpa']['CPA_ID'], currentName: this.currentCpaIndex })
      }
      this.todoSQL.deletion = this.deletedItems
    }
    else if (this.type == 'Process') {
      this.getObjectKeys(this.pppcDataControler).forEach((key: string) => {
        if (this.getObjectKeys(this.callBack).indexOf(key) == -1) {
          this.todoSQL.addition.push({ class: 'Process', unique_id: this.callBack['Process_ID'], attrKey: key, attrValue: this.pppcDataControler[key] })
        }
      })
      this.getObjectKeys(this.callBack).forEach((key: string) => {
        if (!this.arraysAreEqual(this.pppcDataControler[key], this.callBack[key])) {
          this.todoSQL.changeAttr.push({ class: 'Process', unique_id: this.callBack['Process_ID'], attrKey: key, currentValue: this.pppcDataControler[key] })
        }
      })
      if (this.currentFileName != this.callBack['Process_ID']) {
        this.todoSQL.changeName.push({ class: 'Process', unique_id: this.callBack['Process_ID'], currentName: this.currentFileName })
      }
      this.todoSQL.deletion = this.deletedItems
    }
    else if (this.type == 'PreData' || this.type == 'PostData') {
      this.getObjectKeys(this.pppcDataControler).forEach((key: string) => {
        if (this.getObjectKeys(this.callBack).indexOf(key) == -1) {
          this.todoSQL.addition.push({ class: this.type, unique_id: this.callBack['Sample_ID'], attrKey: key, attrValue: this.pppcDataControler[key] })
        }
      })
      this.getObjectKeys(this.callBack).forEach((key: string) => {
        if (!this.arraysAreEqual(this.pppcDataControler[key], this.callBack[key])) {
          this.todoSQL.changeAttr.push({ class: this.type, unique_id: this.callBack['Sample_ID'], attrKey: key, currentValue: this.pppcDataControler[key] })
        }
      })
      if (this.currentFileName != this.callBack['Sample_ID']) {
        this.todoSQL.changeName.push({ class: this.type, unique_id: this.callBack['Sample_ID'], currentName: this.currentFileName })
      }
      this.todoSQL.deletion = this.deletedItems
    }

  }

  returnTask(task:any){
    if (task.nodeClass){
      if (task.attributeKey) {
        this.deletedItems['nodeAttributes'] = this.deletedItems['nodeAttributes'].filter(item => item.attributeKey != task.attributeKey)
      }
      else {
        if (['Experiment', 'Versuch', 'Probe', 'CPA'].indexOf(task['nodeClass']) != -1){
          this.deletedItems['fatherNodes'] = this.deletedItems['fatherNodes'].filter(item => item.Unique_ID != task.Unique_ID)
        }
        else {
          this.deletedItems['childrenNodes'] = this.deletedItems['childrenNodes'].filter(item => item.Unique_ID != task.Unique_ID)
        }
      }
    }
    if (task.attrKey && task.attrValue){
      if (['Process', 'PostData', 'PreData'].indexOf(task.class) != -1){
        delete this.pppcDataControler[task.attrKey]
      }
      else{
        delete this.pppcDataControler[task.class+'*-*'+task.unique_id][task.attrKey]
      }
    }
    if (task.info && task.father){
      if (task.class==='Versuch'){
        this.getObjectKeys(this.addControler).forEach(itemKey=>{
          if (this.addControler[itemKey]['Versuche ID'] == task.info['Versuche ID']){
            delete this.addControler[itemKey]
          }
        })
      }
      else if (task.class === 'Probe'){
        this.addControlerProbe[task.father.Unique_ID] = this.addControlerProbe[task.father.Unique_ID].filter((item:any) => item['Sample ID'] != task.info['Sample ID'])
      }
      else {
        delete this.addControler[task.class]
      }
    }
    if (task.currentName) {
      if (task.class === 'Probe' || task.class === 'Versuch'){
        this.currentSubName[task.unique_id] = this.getLastItemAfterSplit(task.unique_id, '*-*')
      }
      else if (task.class === 'PreData' || task.class === 'PostData') {
        this.currentFileName = this.callBack['Sample_ID']
      }
      else if (task.class === 'Process') {
        this.currentFileName = this.callBack['Process_ID']
      }
      else if (task.class === 'CPA') {
        this.currentCpaIndex = this.callBack['cpa']['CPA_ID']
      }
      else if (task.class === 'Experiment') {
        this.currentFileName = this.callBack['experiment']['Experiment_ID']
      }
      else {
        this.currentSubName[task.class+'*-*'+task.unique_id] = this.getLastItemAfterSplit(task.unique_id, '*-*')
      }
    }
    if (task.currentValue) {
      if (task.class === 'Process' || task.class === 'PreData' || task.class === 'PostData') {
        this.pppcDataControler[task.attrKey] = cloneDeep(this.callBack[task.attrKey])
      }
      else if (task.class === 'Probe'){
        this.pppcDataControler[task.unique_id][task.attrKey] = cloneDeep(this.pppcDataMemory[task.unique_id][task.attrKey])
      }
      else {
        this.pppcDataControler[task.class+'*-*'+task.unique_id][task.attrKey] = cloneDeep(this.pppcDataMemory[task.class+'*-*'+task.unique_id][task.attrKey])
      }
      
    }
    this.generateCommit()
  }

  commit (){
    this.undoDisabled = true
    this.queryNeo4jService.addDelModi(this.todoSQL).then((res:any)=>{
      this.resultStatus = true
      this.response = res
    })
  }

  getLastItemAfterSplit(inputString: string, delimiter: string): string {
    const parts = inputString.split(delimiter);
    return parts[parts.length - 1];
  }

}
