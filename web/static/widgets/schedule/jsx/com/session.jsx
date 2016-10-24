import React from 'react';
import utf8  from 'utf8';

import visualConfig from './day_schedule_config.jsx';


export default class Session extends React.Component {
    constructor() {
        super();

        this.state = {
            hover: false,
        };
    }

    render() {
        let zeroTimestamp = this.props.zeroTimestamp;
        let timestamp     = this.props.timestamp;
        let session       = this.props.session;
        let rooms         = this.props.rooms;

        let room             = this._room(rooms, session.room);
        let trackIndex       = this._roomIndex(rooms, session.room);
        let durationInMinute = session.durationInMinute;
        let progressInMinute = (timestamp - zeroTimestamp) / 1000 / 60;
        let heightPerMinute  = visualConfig.heightPerMinute;

        if (this.state.hover && durationInMinute < 30) {
            heightPerMinute *= visualConfig.shortSessionHeightBooster;
        }

        let originXOffset    = (100 / rooms.length) * trackIndex;
        let blockTop         = (visualConfig.heightPerMinute * progressInMinute) + 1;
        let blockWidth       = ((100 / rooms.length) - visualConfig.rightMargin);
        let blockHeight      = (heightPerMinute * durationInMinute) - visualConfig.bottomMargin;
        let readableTime     = timestamp.format(visualConfig.timeFormat);
        let roomCode         = session.room || 'general';
        let roomName         = room ? room.name : '';

        if (trackIndex === null) {
            blockWidth = 100;
        }

        let forceStyle = {
            zIndex : this.state.hover ? 1 : 0,
            left   : originXOffset + '%',
            width  : blockWidth    + '%',
            height : blockHeight   + 'px',
            top    : blockTop      + 'px',
        };

        return (
            <div
                className   = { ['session', this.state.hover ? 'hover' : ''].join(' ') }
                data-key    = { session.alias }
                data-time   = { readableTime }
                data-room   = { roomCode }
                style       = { forceStyle }
                onMouseOver = { this._onMouseOver.bind(this) }
                onMouseOut  = { this._onMouseOut.bind(this) }
            >
                <div className="inner">
                    <div className="room">{ roomName }</div>
                    <div className="title">{ session.title }</div>
                    <div className="speakers">{ session.speakers }</div>
                    <div className="period">
                        <span className="start">{ session.mStartTime.format(visualConfig.timeFormat) }</span>
                        <span className="end">{ session.mEndTime.format(visualConfig.timeFormat) }</span>
                    </div>
                </div>
            </div>
        );
    }

    _onMouseOver() {
        this.setState({hover: true});
    }

    _onMouseOut() {
        this.setState({hover: false});
    }

    _roomIndex(rooms, roomCode) {
        let index = 0;

        for (let room of rooms) {
            if (room.slug === roomCode) {
                return index;
            }

            index++;
        }

        return null;
    }

    _room(rooms, roomCode) {
        for (let room of rooms) {
            if (room.slug === roomCode) {
                return room;
            }
        }

        return null;
    }
}
