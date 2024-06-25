import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'excludeItem'
})
export class ExcludeItemPipe implements PipeTransform {
    transform(arr: any[], itemsToExclude: any[]): any[] {
        if (!Array.isArray(arr)) {
            return arr;
        }

        return arr.filter(item => !itemsToExclude.includes(item));
    }
}