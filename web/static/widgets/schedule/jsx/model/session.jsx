import marked from 'marked';
import moment from 'moment';
import utf8   from 'utf8';
import wtf8   from 'wtf-8';

let PARSIBLE_TIME_FORMAT = 'YYYY-MM-DD HH:mm'; // ISO format
let SORTABLE_TIME_FORMAT = 'X'; // UNIX timestamp
let reNewLine = /\n+/g;


export default class Session {
    constructor(title, speakers, alias, room, startTime, endTime, originalSummary) {
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

        this.originalSummary    = originalSummary;
        this._cachedHTMLSummary = null;
    }

    get durationInMinute() {
        return this.duration / 60;
    }

    get html() {
        if (!this.originalSummary) {
            return null;
        }

        if (!this._cachedHTMLSummary) {
            this._cachedHTMLSummary = marked(this.originalSummary);
            this._cachedHTMLSummary = this._cachedHTMLSummary.replace(reNewLine, ' ');

            try {
                this._cachedHTMLSummary = utf8.decode(this._cachedHTMLSummary);
            } catch (e) {
                this._cachedHTMLSummary = this._cachedHTMLSummary;
            }
        }

        return this._cachedHTMLSummary;
    }
}
