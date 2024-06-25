import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-seite-welcome',
  templateUrl: './seite-welcome.component.html',
  styleUrls: ['./seite-welcome.component.css']
})
export class SeiteWelcomeComponent {
  @Input() side: boolean = false
  @Input() highlight: string = 'none'
  resourcesCards: { href: string, icon: string, span: string }[] = [
    { href: 'about-us', icon: 'perm_identity', span: 'About Us' },
    { href: 'about-this', icon: 'help_outline', span: 'About This' },
    { href: 'technology', icon: 'developer_board', span: 'Technology' },
    { href: 'database', icon: 'cloud_queue', span: 'Database' },
    { href: 'nn', icon: 'blur_on', span: 'Neural Networks' }
  ]

  functionCards: { icon: string, span: string, href: string }[] = [
    { icon: 'storage', span: 'Data storage', href: 'start/data-storage' },
    { icon: 'insert_chart_outlined', span: 'Data analyse', href: 'start/data-analyse' },
    { icon: 'center_focus_weak', span: 'Cells count', href: 'start/cells-count' },
    { icon: 'bubble_chart', span: 'Survivalrate predict', href: 'start/survivalrate-predict' },
    { icon: 'trending_up', span: 'Parameter optimize', href: 'start/parameter-optimize' },
    { icon: 'favorite_border', span: 'Feedback', href: 'start/feedback' }
  ]

  check(input:string){
    return `/${input}` === this.highlight
  }

}
