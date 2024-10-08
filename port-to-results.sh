#!/usr/bin/env bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

source "${SCRIPTDIR}/bin/includes/bashcolors.sh"
source "${SCRIPTDIR}/bin/includes/logging.sh"

content_dir="content"

# Initialize empty associative arrays
declare -A groupIdSet
declare -A artifactIdSet

project_count=0
max_projects=$1
echo "Max projects: $max_projects"

for buildspec in $(find $content_dir -name "*.buildspec")
do

    # Source the buildspec file
    source $buildspec

    if [[ $groupId == "io.fabric8" ]]
    then
        continue
    fi

    if [[ "${jdk}" == ??.0.* || -n "${RB_SHELL}" || ${command} == SHELL* ]]
    then
        continue
    fi

    # Check if this is a Maven project
    if [[ "$tool" != "mvn" ]]
    then
        info "Skipping $buildspec as it's not a Maven project"
        continue
    fi

    # Check if we've already processed this groupId/artifactId combination
    if [[ -n ${groupIdSet[$groupId]} && -n ${artifactIdSet[$artifactId]} ]]
    then
        info "Skipping $buildspec as we have one version of this artifact"
        continue
    fi

    groupIdSet[$groupId]=1
    artifactIdSet[$artifactId]=1

    mkdir -p results/$groupId/$artifactId/$version
    cp $buildspec results/$groupId/$artifactId/$version

    info "Processed Maven project: $groupId:$artifactId:$version"

    
    if [[ -n "$max_projects" ]]; then
        if (( project_count >= max_projects )); then
            info "Reached maximum number of Maven projects ($max_projects). Stopping."
            break
        fi
    fi
    
    # Increment project count
    ((project_count++))

done

echo "Total projects processed: $project_count"

