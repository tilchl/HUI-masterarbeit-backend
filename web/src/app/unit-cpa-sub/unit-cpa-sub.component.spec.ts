import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitCpaSubComponent } from './unit-cpa-sub.component';

describe('UnitCpaSubComponent', () => {
  let component: UnitCpaSubComponent;
  let fixture: ComponentFixture<UnitCpaSubComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitCpaSubComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitCpaSubComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
