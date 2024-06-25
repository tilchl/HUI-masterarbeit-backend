import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitEditExcelComponent } from './unit-edit-excel.component';

describe('UnitEditExcelComponent', () => {
  let component: UnitEditExcelComponent;
  let fixture: ComponentFixture<UnitEditExcelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitEditExcelComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitEditExcelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
