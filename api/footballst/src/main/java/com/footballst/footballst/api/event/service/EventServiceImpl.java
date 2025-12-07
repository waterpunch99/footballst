package com.footballst.footballst.api.event.service;

import com.footballst.footballst.api.event.Event;
import com.footballst.footballst.api.event.EventRepository;
import com.footballst.footballst.api.event.dto.EventResponseDto;
import com.footballst.footballst.api.matchDetail.MatchDetail;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;


@RequiredArgsConstructor
@Service
public class EventServiceImpl implements EventService {

    private final EventRepository eventRepository;

    @Override
    public List<EventResponseDto> getEventsByMatch(Long matchId) {
        return eventRepository.findByMatchId(matchId)
                .stream()
                .map(EventResponseDto::fromEntity)
                .toList();
    }
}
