import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteDataAnalyseComponent } from './seite-data-analyse.component';

describe('SeiteDataAnalyseComponent', () => {
  let component: SeiteDataAnalyseComponent;
  let fixture: ComponentFixture<SeiteDataAnalyseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteDataAnalyseComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteDataAnalyseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
