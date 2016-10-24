import moment  from 'moment';
import Session from '../model/session.jsx';

let DEFAULT_ROOM = 'general';


export default class Analyzer {
    objectifySessions(scheduleData, talkData) {
        let days = [];

        for (let day of scheduleData) {
            let date       = day.date;
            let collection = {
                date     : date,
                sessions : [],
            };

            days.push(collection);

            for (let entry of day.entries) {
                let startTime = [date, entry.start_time].join(' ');

                // General events
                if (entry.title) {
                    collection.sessions.push(
                        new Session(
                            entry.title,
                            null,
                            null,
                            null,
                            startTime,
                            [date, entry.end_time].join(' ')
                        )
                    );

                    continue;
                }

                // Talks and tutorials
                for (let room in entry.talks) {
                    let alias = entry.talks[room];
                    let talk  = talkData[alias + '_en'];
                    // console.log(room, alias || 'N/A', talk || 'MIA');

                    if (alias.length === 0) {
                        continue;
                    }

                    collection.sessions.push(
                        new Session(
                            talk.title,
                            talk.speakers,
                            alias,
                            room,
                            startTime,
                            [date, talk.end_time].join(' ')
                        )
                    );
                }
            }
        }

        // console.log(days);

        return days;
    }

    analyzeTimeline(days) {
        let dates    = [];
        let schedule = {};

        for (let day of days) {
            let sessions = day.sessions;
            let date     = sessions[0].mStartTime.format('YYYY-MM-DD');

            let timePoints     = [];
            let timeToSessions = {};

            dates.push(date);

            schedule[date] = {
                label    : date,
                duration : null,
                points   : timePoints,
                sessions : timeToSessions,
            };

            for (let session of sessions) {
                let room      = session.room || DEFAULT_ROOM;
                let startTime = session.startTime;
                let endTime   = session.endTime;

                let timeNotRegistered = timePoints.indexOf(startTime) < 0;

                if (timeNotRegistered) {
                    timePoints.push(startTime);
                }

                if (!timeToSessions[startTime]) {
                    timeToSessions[startTime] = {};
                }

                timeToSessions[startTime][room] = session;

                if (timePoints.indexOf(endTime) < 0) {
                    timePoints.push(endTime);
                }
            }
        }

        dates.sort();

        for (let date in schedule) {
            let day = schedule[date];

            day.points.sort();
            day.duration = (moment(day.points[day.points.length - 1]) - moment(day.points[0])) / 1000;
        }

        return {
            dates    : dates,
            schedule : schedule,
        };
    }
}
