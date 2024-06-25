import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitBackendCheckComponent } from './unit-backend-check.component';

describe('UnitBackendCheckComponent', () => {
  let component: UnitBackendCheckComponent;
  let fixture: ComponentFixture<UnitBackendCheckComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitBackendCheckComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitBackendCheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
