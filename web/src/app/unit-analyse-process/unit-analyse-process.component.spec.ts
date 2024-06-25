import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitAnalyseProcessComponent } from './unit-analyse-process.component';

describe('UnitAnalyseProcessComponent', () => {
  let component: UnitAnalyseProcessComponent;
  let fixture: ComponentFixture<UnitAnalyseProcessComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitAnalyseProcessComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitAnalyseProcessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
