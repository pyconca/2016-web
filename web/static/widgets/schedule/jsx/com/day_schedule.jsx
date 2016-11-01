import moment from 'moment';
import React  from 'react';

import Info         from './info.jsx';
import Session      from './session.jsx';
import visualConfig from './day_schedule_config.jsx';

let reDate = /^[^ ] /;


export default class DaySchedule extends React.Component {
    constructor() {
        super();

        this.state = {
            opened: null,
        };
    }

    render() {
        let schedule         = this.props.schedule;
        let rooms            = this.props.rooms;
        let durationInMinute = schedule.duration / 60;
        let timelineHeight   = (visualConfig.heightPerMinute * durationInMinute) + visualConfig.extraPadding;

        let forceStyle = {
            height   : timelineHeight + 'px',
        };

        $('body').css({overflow: this.state.opened ? 'hidden' : 'auto'});

        return (
            <div className="day" data-date={ schedule.label } style={ forceStyle }>
                { this._renderOverlayInformation() }
                { this._renderTimeLabels(schedule) }

                <div className="sessions">
                    { this._renderSessions(schedule, rooms) }
                </div>
            </div>
        );
    }

    _renderOverlayInformation() {
        if (!this.state.opened) {
            return '';
        }

        return (
            <Info
                onClick = { this._onClickCloseInfo.bind(this) }
                room    = { this.state.opened.room }
                session = { this.state.opened.session }
            />
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
                        onClick       = { this._onClickOpenInfo.bind(this) }
                    />
                );
            }
        }

        return renderedSessions;
    }

    _onClickOpenInfo(session) {
        this.setState({ opened: session });
    }

    _onClickCloseInfo(session) {
        this.setState({ opened: null });
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
