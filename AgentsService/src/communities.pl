/** <module> This file handles managing communities and generations in the service
 * @author James King
 */

/**
 * new_community(--ID:int) is det
 *
 * Create a new community in the system with an autogenerated and returned ID.
 *
 * @arg ID The ID of the new created community
 */

:- dynamic community/1, generation/2, id_gap/1, id/1.
:- multifile community/1, generation/2.
?- ['./agents'].
:- use_module(library(error), [existence_error/2]).


new_community(ID):-
	get_new_id(ID),
	assert(community(ID)).

/**
 * retract_community(++DictIn:dict, -Success:atom) is semidet
 *
 * Retracts a community and all it's agents and generations from the system, the community id is stored in the dict.
 *
 * @arg DictIn Contains the id of the community to delete.
 */

retract_community(ID, Success):-
	community(ID), !,
	retract_agents(ID),
	retract_generations(ID),
	retract(community(ID)),
	assert(id_gap(ID)),
	Success = true.
retract_community(_, Success):-
	Success = "No community with this ID to retract".

/**
 * get_new_id(--NewID:int) is det
 *
 * Get the next id for a new community
 *
 * @arg ID The ID for the community
 */

% Get a community id for an unfilled gap
get_new_id(ID):-
	id_gap(ID), !,
	retract(id_gap(ID)).
% Get a new community id as there is no unfilled gaps
get_new_id(NewID):-
	current_predicate(id/1),
	id(ID), !,
	retract(id(ID)),
	NewID is ID+1,
	assert(id(NewID)).
get_new_id(ID):-
	assert(id(0)),
	ID is 0.

/**
 * new_generation(++DictIn:dict, --Success:atom) is nondet
 *
 * Create a new generation in the community with the specified community id and generation id,
 * The api docs specify the layout of the dictionary.
 *
 * @arg DictIn The dictionary containing the two ids
 * @arg Success True if the creation is successful, error message if not
 */

% Create a new generation, if one with the same community and generation ID doesn't already exist
new_generation(DictIn, Success):-
	% Check if the dictionary is of the correct form
	_{community: _, generation: _} :< DictIn,
	current_predicate(generation/2),
	current_predicate(community/1),
	CommunityID = DictIn.community,
	community(CommunityID),
	GenerationID = DictIn.generation,
	(generation(community(CommunityID), GenerationID) -> Success = "This community already has a generation with this id", !, true ;
	assert(generation(community(CommunityID), GenerationID)),
	Success = true), !.
% Create the first generation in the system
new_generation(DictIn, Success):-
	% Check if the dictionary is of the correct form
	_{community: _, generation: _} :< DictIn,
    \+current_predicate(generation/2),
	current_predicate(community/1),
	CommunityID = DictIn.community,
	community(CommunityID),
	GenerationID = DictIn.generation,
	assert(generation(community(CommunityID), GenerationID)),
	Success = true, !.
% Fail nicely when there is no such community
new_generation(DictIn, Success):-
	% Check if the dictionary is of the correct form
	_{community: _, generation: _} :< DictIn,
	current_predicate(community/1),
	CommunityID = DictIn.community,
	\+community(CommunityID),
	Success = "No such community", !.
% If the input doesn't contain a community or generation entry
new_generation(DictIn, Success):-
	\+ _{community: _} :< DictIn,
	\+ _{generation: _} :< DictIn,
	Success = "Incorrect input, no community or generation fields", !.
% If the input doesn't contain a community entry
new_generation(DictIn, Success):-
	\+ _{community: _} :< DictIn,
	Success = "Incorrect input, no community field", !.
% If the input doesn't contain a generation entry
new_generation(DictIn, Success):-
	\+ _{generation: _} :< DictIn,
	Success = "Incorrect input, no generation field", !.


/**
 * retract_generations(++ID:int) is nondet
 *
 * Delete all generations related to the community ID given.
 *
 * @arg ID The id of the community related to these generations we are deleting
 */
retract_generations(ID):-
	forall(generation(community(ID), GenID), (retract(generation(community(ID), GenID)))).
