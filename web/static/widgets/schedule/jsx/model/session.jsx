import moment from 'moment';
import utf8   from 'utf8';

let PARSIBLE_TIME_FORMAT = 'YYYY-MM-DD HH:mm'; // ISO format
let SORTABLE_TIME_FORMAT = 'X'; // UNIX timestamp


export default class Session {
    constructor(title, speakers, alias, room, startTime, endTime) {
        this.title      = title;
        this.speakers   = speakers ? utf8.decode(speakers) : null;
        this.alias      = alias;
        this.room       = room;
        this.startTime  = startTime;
        this.endTime    = endTime;
        this.mStartTime = moment(startTime);
        this.mEndTime   = moment(endTime);
        this.uStartTime = parseInt(this.mStartTime.format(SORTABLE_TIME_FORMAT), 10);
        this.uEndTime   = parseInt(this.mEndTime.format(SORTABLE_TIME_FORMAT), 10);
        this.duration   = this.uEndTime - this.uStartTime;
    }

    get durationInMinute() {
        return this.duration / 60;
    }
}
