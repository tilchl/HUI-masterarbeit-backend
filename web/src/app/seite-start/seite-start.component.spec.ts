import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteStartComponent } from './seite-start.component';

describe('SeiteStartComponent', () => {
  let component: SeiteStartComponent;
  let fixture: ComponentFixture<SeiteStartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteStartComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteStartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
