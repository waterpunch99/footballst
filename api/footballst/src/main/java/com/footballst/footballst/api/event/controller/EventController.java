package com.footballst.footballst.api.event.controller;

import com.footballst.footballst.api.event.dto.EventResponseDto;
import com.footballst.footballst.api.event.service.EventService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventService eventService;


    @GetMapping("/{matchId}")
    public ResponseEntity<List<EventResponseDto>> getEvents(@PathVariable Long matchId) {
        return ResponseEntity.ok(eventService.getEventsByMatch(matchId));
    }
}
