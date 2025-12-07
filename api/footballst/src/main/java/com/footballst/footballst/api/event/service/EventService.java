package com.footballst.footballst.api.event.service;

import com.footballst.footballst.api.event.dto.EventResponseDto;

import java.util.List;

public interface EventService {
    List<EventResponseDto> getEventsByMatch(Long matchId);
}
