import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteWelcomeComponent } from './seite-welcome.component';

describe('SeiteWelcomeComponent', () => {
  let component: SeiteWelcomeComponent;
  let fixture: ComponentFixture<SeiteWelcomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteWelcomeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteWelcomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
