import moment from 'moment';
import React  from 'react';

import Session      from './session.jsx';
import visualConfig from './day_schedule_config.jsx';

let reDate = /^[^ ] /;


export default class DaySchedule extends React.Component {
    render() {
        let schedule         = this.props.schedule;
        let rooms            = this.props.rooms;
        let durationInMinute = schedule.duration / 60;
        let timelineHeight   = (visualConfig.heightPerMinute * durationInMinute) + visualConfig.extraPadding;

        let forceStyle = {
            height: timelineHeight + 'px',
        };

        return (
            <div className="day" data-date={ schedule.label } style={ forceStyle }>
                { this._renderTimeLabels(schedule) }

                <div className="sessions">
                    { this._renderSessions(schedule, rooms) }
                </div>
            </div>
        );
    }

    _renderSessions(schedule, rooms) {
        let zeroTimestamp    = moment(schedule.points[0]);
        let renderedSessions = [];
        let lastLocalId      = 0;

        for (let point of schedule.points) {
            let timestamp = moment(point);
            let sessions  = schedule.sessions[point];

            if (!sessions) {
                continue;
            }

            renderedSessions.push(
                <div
                    key       = { ++lastLocalId }
                    className = "start-timestamp"
                    title     = { timestamp.format('YYYY-MM-DD HH:mm') }
                >
                    { timestamp.format(visualConfig.timeFormat) }
                </div>
            );

            for (let roomCode in sessions) {
                renderedSessions.push(
                    <Session
                        key           = { ++lastLocalId }
                        zeroTimestamp = { zeroTimestamp }
                        timestamp     = { timestamp }
                        session       = { sessions[roomCode] }
                        rooms         = { rooms }
                    />
                );
            }
        }

        return renderedSessions;
    }

    _renderTimeLabels(schedule) {
        let zeroTimestamp = moment(schedule.points[0]);
        let timeLabels    = [];

        for (let point of schedule.points) {
            let timestamp = moment(point);

            timeLabels.push(this._renderTimeLabel(zeroTimestamp, timestamp));
        }

        return timeLabels;
    }

    _renderTimeLabel(zeroTimestamp, timestamp) {
        let durationInMinute = (timestamp - zeroTimestamp) / 1000 / 60;
        let forceStyle       = {
            top: (visualConfig.heightPerMinute * durationInMinute) + 'px',
        };

        return (
            <div
                key       = { timestamp }
                className = "time-label"
                data-time = { timestamp.format(visualConfig.timeFormat) }
                style     = { forceStyle }
                title     = { timestamp.format('YYYY-MM-DD HH:mm') }
            />
        );
    }
}
