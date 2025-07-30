# initial screen
screen lab_hallway_screen:
    image "lab_hallway_dim"
    hbox:
        xpos 0.20 yalign 0.5
        imagebutton:
            idle "data_analysis_lab_idle"
            hover "data_analysis_lab_hover"
            hovered Notify("Data Analysis Lab")
            unhovered Notify('')
            action Jump('data_analysis_lab')
    hbox:
        xpos 0.55 yalign 0.48
        imagebutton:
            idle "materials_lab_idle"
            hover "materials_lab_hover"
            hovered Notify("Materials Lab")
            unhovered Notify('')
            action Jump('materials_lab')

############################## DATA ANALYSIS ##############################
screen data_analysis_lab_screen:
    image "afis_interface"
    # hbox:
    #     xpos 0.25 yalign 0.25
    #     imagebutton:
    #         idle "afis_software_idle"
    #         hover "afis_software_hover"
    #         hovered Notify("AFIS Software")
    #         unhovered Notify('')
    #         action Jump('afis')
    hbox:
        xpos 0.25 yalign 0.25
        imagebutton:
            idle "dna_software_idle"
            hover "dna_software_hover"
            hovered Notify("CODIS DNA Analysis Software")
            unhovered Notify('')
            action Jump('dna_analysis')

screen afis_screen:
    default afis_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default interface_search = False
    image afis_bg

    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Import'):
            style "afis_button"
            action [
                ToggleLocalVariable('interface_import'),
                Show("inventory"), Hide("toolbox"),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('interface_search', False),
                SetLocalVariable('afis_bg', 'software_interface'),
                Function(set_cursor, '')]
    
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Search'):
            sensitive not interface_search
            style "afis_button"
            action [
                ToggleLocalVariable('interface_search'),
                SetLocalVariable('afis_bg', 'software_search'),
                Function(calculate_afis, current_evidence),
                Function(set_cursor, '')]
    
    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            
            ## add in sensitive when clicked on evidence 


            hotspot (282,241,680,756) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                Function(set_cursor, '')]

    showif interface_imported:
        hbox:
            xpos current_evidence.afis_details['xpos'] ypos current_evidence.afis_details['ypos']
            image current_evidence.afis_details['image']
    
    showif interface_search:
        if afis_search:
            for i in range(len(afis_search)):
                hbox:
                    xpos afis_search_coordinates[i]['xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].name+"{/color}")
                hbox:
                    xpos afis_search_coordinates[i]['score_xpos'] ypos afis_search_coordinates[i]['ypos']
                    hbox:
                        text("{color=#000000}"+afis_search[i].afis_details['score']+"{/color}")
            
        else:
            hbox:
                xpos 0.57 yalign 0.85
                hbox:
                    text("{color=#000000}No match found in records.{/color}")

screen dna_analysis_screen:
    default dna_bg = "software_interface"
    default interface_import = False
    default interface_imported = False
    default selected_warrant = ""
    default selected_evidence = ""
    image dna_bg

    # Warrant samples section (right side)
    vbox:
        xpos 0.62 ypos 0.206
        text "{color=#ffffff}Warrant Samples{/color}" size 22
        
    hbox:
        xpos 0.49 ypos 0.225
        spacing -20
        textbutton "Male Suspect":
            style "afis_button"
            action [SetLocalVariable('selected_warrant', 'male')]
        
        textbutton "Female Suspect":
            style "afis_button"
            action [SetLocalVariable('selected_warrant', 'female')]
    
    # Display warrant sample DNA profile image
    if selected_warrant != "":
        vbox:
            xpos 0.55 ypos 0.28
            text "{color=#000000}DNA Profile:{/color}" size 16
            if selected_warrant == "male":
                # Placeholder image for male DNA profile
                add "images/data_analysis_lab/male_dna_profile.jpg" at Transform(zoom=0.475)
                # text "{color=#000000}Male Suspect DNA Profile{/color}" size 14
            elif selected_warrant == "female":
                # Placeholder image for female DNA profile
                add "images/data_analysis_lab/female_dna_profile.jpg" at Transform(zoom=0.462)
                # text "{color=#000000}Female Suspect DNA Profile{/color}" size 14

    # Import evidence section (left side)
    hbox:
        xpos 0.15 ypos 0.145
        textbutton('Import Evidence'):
            style "afis_button"
            action [
                ToggleLocalVariable('interface_import'),
                Show("inventory"), Hide("toolbox"),
                SetLocalVariable('interface_imported', False),
                SetVariable('dna_comparison_result', ''),
                Function(set_cursor, '')]
    
    # Compare button
    hbox:
        xpos 0.35 ypos 0.145
        textbutton('Compare'):
            sensitive interface_imported and selected_warrant != "" and selected_evidence != ""
            style "afis_button"
            action [
                Hide("inventory"),
                Function(compare_dna_profiles, selected_evidence, selected_warrant),
                Function(set_cursor, '')]
    
    # Exclude mixed sample button
    hbox:
        xpos 0.55 ypos 0.145
        textbutton('Discard Evidence'):
            sensitive interface_imported and selected_evidence == "mixed_dna_profile"
            style "afis_button"
            action [
                Function(discard_mixed_sample, selected_evidence),
                SetLocalVariable('interface_imported', False),
                SetLocalVariable('selected_evidence', ""),
                SetVariable('dna_comparison_result', 'Mixed sample excluded from analysis.'),
                Function(set_cursor, '')]

    showif interface_import:
        imagemap:
            idle "software_interface"
            hover "software_import_hover"
            
            hotspot (294, 249, 660, 734) action [
                SetLocalVariable('interface_import', False), 
                SetLocalVariable('interface_imported', True),
                SetLocalVariable('selected_evidence', item_dragged if item_dragged != '' else 'none'),
                Function(set_cursor, '')]

    showif interface_imported and selected_evidence != "":
        vbox:
            xpos 0.16 ypos 0.235
            text "{color=#000000}Evidence DNA Profile:{/color}" size 16
            if selected_evidence != "none":
                text "{color=#000000}Loaded: [get_dna_display_name(selected_evidence)]{/color}" size 14
                if selected_evidence == "male_dna_profile":
                    add "images/data_analysis_lab/male_dna_profile.jpg" at Transform(zoom=0.475)
                elif selected_evidence == "female_dna_profile":
                    add "images/data_analysis_lab/female_dna_profile.jpg" at Transform(zoom=0.462)
                elif selected_evidence == "mixed_dna_profile":
                    add "images/data_analysis_lab/mixed_dna_profile.jpg" at Transform(zoom=0.475)
                else:
                    # Fallback for any other evidence types
                    add "gui/frame.png" at Transform(zoom=0.4)
                    text "{color=#000000}DNA profile image not available{/color}" size 12
            else:
                text "{color=#000000}No DNA evidence selected{/color}" size 16
    
    if dna_comparison_result != "":
        hbox:
            xpos 0.21 ypos 0.871
            vbox:
                text "{color=#000000}Analysis Result:{/color}" size 18
                text "{color=#000000}[dna_comparison_result]{/color}" size 16
screen materials_lab_screen:
    image "materials_lab"

    # hbox:
    #     xpos 0.15 yalign 0.5
    #     imagebutton:
    #         idle "fumehood_idle" at Transform(zoom=0.8)
    #         hover "fumehood_hover"
    #         hovered Notify("Fume Hood")
    #         unhovered Notify('')
    #         action Jump('fumehood')
    # hbox:
    #     #xpos 0.4 yalign 0.5
    #     xpos 0.32 yalign 0.5
    #     imagebutton:
    #         idle "fingerprint_development_idle" at Transform(zoom=0.8)
    #         hover "fingerprint_development_hover"
    #         hovered Notify("Fingerprint Development")
    #         unhovered Notify('')
    #         action NullAction()
    
    # hbox:
    #     #xpos 0.4 yalign 0.5
    #     xpos 0.48 yalign 0.53
    #     imagebutton:
    #         idle "lab_bench_idle" at Transform(zoom=0.8)
    #         hover "lab_bench_hover"
    #         hovered Notify("Lab Bench")
    #         unhovered Notify('')
    #         action NullAction()
    
    hbox:
        xpos 0.62 yalign 0.5
        imagebutton:
            idle "analytical_instruments_idle"
            hover "analytical_instruments_hover"
            hovered Notify("Analytical Instruments")
            unhovered Notify('')
            action Jump('analytical_instruments')

screen fumehood_screen:
    image "fumehood"

screen analytical_instruments_screen:
    image "lab_bench"
    imagebutton:
        idle "pcr_machine"
        hover "pcr_machine"
        at pcr_machine_transform
        hovered Notify("PCR Machine")
        unhovered Notify('')
        action Jump('pcr_machine')

transform pcr_machine_transform:
    zoom 0.2
    xpos 0.2225
    ypos 0.29

screen pcr_machine_screen:
    # DNA extraction and PCR amplification process with lab assistant guidance
    image "empty_lab_bench"
    
    # Show PCR machine state
    if pcr_state == "empty":
        image "empty_pcr" at pcr_display_transform
    elif pcr_state == "filled":
        image "filled_pcr" at pcr_display_transform
    
    # Track mistakes for final summary
    # pcr_mistakes is a list that accumulates errors
    
    # Lab assistant dialogue and questions
    if pcr_step == 0:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: We need to extract and amplify DNA from this blood swab sample."
            text "First, we'll prepare the sample. What volumes do we need?"
            text "We need: 200µl whole blood, QIAGEN Protease, and Buffer AL."
            
            # Randomize button order
            $ step0_buttons = [
                ("20µl Protease, 200µl Buffer AL", [SetVariable("pcr_step", 1), SetVariable("pcr_state", "filled")]),
                ("50µl Protease, 100µl Buffer AL", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Incorrect protease/buffer volumes. The proper amounts are 20µl Protease and 200µl Buffer AL.")])
            ]
            $ import random
            $ random.shuffle(step0_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step0_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 1:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Good! Now we mix by vortexing and incubate."
            text "What temperature should we use for incubation?"
            
            # Randomize button order
            $ step1_buttons = [
                ("37°C for 15 minutes", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Incorrect incubation temperature. We need 56°C for 10 minutes to properly lyse the cells.")]),
                ("56°C for 10 minutes", [SetVariable("pcr_step", 2)]),
                ("95°C for 5 minutes", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "That's the PCR denaturation temperature, not for sample incubation. We need 56°C for 10 minutes.")])
            ]
            $ random.shuffle(step1_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step1_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 2:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: After incubation and spinning down, we add ethanol."
            text "What concentration of ethanol should we use?"
            
            # Randomize button order
            $ step2_buttons = [
                ("70% ethanol", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "70% ethanol is too dilute. We need 96-100% ethanol for proper DNA precipitation.")]),
                ("96-100% ethanol", [SetVariable("pcr_step", 3)]),
                ("50% ethanol", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "50% ethanol concentration is far too low. We need 96-100% ethanol.")])
            ]
            $ random.shuffle(step2_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step2_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 3:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Now we apply the mixture to the QIAamp spin column."
            text "The DNA binds to the filter. Next, we wash with Buffer AW1."
            text "How much Buffer AW1 should we add?"
            
            # Randomize button order
            $ step3_buttons = [
                ("200µl Buffer AW1", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Insufficient buffer volume. We need 500µl Buffer AW1 for proper washing.")]),
                ("500µl Buffer AW1", [SetVariable("pcr_step", 4)]),
                ("1000µl Buffer AW1", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Excessive buffer volume could damage the column. We need exactly 500µl Buffer AW1.")])
            ]
            $ random.shuffle(step3_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step3_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 4:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: After washing with AW1, we use Buffer AW2."
            text "How long should we centrifuge with AW2?"
            
            # Randomize button order
            $ step4_buttons = [
                ("1 minute", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Insufficient centrifugation time. Buffer AW2 requires 3 minutes for complete salt removal.")]),
                ("3 minutes", [SetVariable("pcr_step", 5)]),
                ("10 minutes", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Excessive centrifugation time could damage the DNA. 3 minutes is optimal.")])
            ]
            $ random.shuffle(step4_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step4_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 5:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Finally, we elute the DNA with Buffer AE."
            text "How much DNA should we use for a 50µl PCR reaction?"
            
            # Randomize button order
            $ step5_buttons = [
                ("5µl extracted DNA", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Too much DNA will inhibit the PCR reaction. Use only 1µl for a 50µl reaction.")]),
                ("1µl extracted DNA", [SetVariable("pcr_step", 6)]),
                ("10µl extracted DNA", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Excessive DNA amount will completely inhibit PCR. Use only 1µl.")])
            ]
            $ random.shuffle(step5_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step5_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 6:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Perfect! The PCR amplification is complete."
            text "Now we need to compare this DNA profile to a reference sample."
            text "What should we compare it against?"
            
            # Randomize button order
            $ step6_buttons = [
                ("Random database profiles", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "Incorrect comparison method. We need a specific suspect sample obtained legally.")]),
                ("Blood from accused via warrant", [SetVariable("pcr_step", 7)]),
                ("Any available samples", [SetVariable("pcr_step", -1), SetVariable("pcr_error", "No proper legal authorization. We need blood from the accused obtained via proper warrant.")])
            ]
            $ random.shuffle(step6_buttons)
            
            hbox:
                xalign 0.5
                spacing 20
                for button_text, button_action in step6_buttons:
                    textbutton button_text:
                        style "back_button"
                        action button_action
    
    elif pcr_step == 7:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Excellent work! You completed the DNA extraction"
            text "and PCR amplification process perfectly."
            
            textbutton "Complete Analysis":
                style "back_button"
                xalign 0.5
                action [SetVariable("pcr_step", 8)]
    
    elif pcr_step == 8:
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: Okay, now let me get through the rest of the swabs."
            text "Great! But we have three profiles... I thought there were only two people involved?"
            text "Anyway, they've been added to your evidence toolbox for analysis."
            
            textbutton "Continue":
                style "back_button"
                xalign 0.5
                action [SetVariable("pcr_step", 0), SetVariable("pcr_state", "empty"),
                        Function(add_dna_samples), Jump('analytical_instruments')]
    
    elif pcr_step == -1:  # Error state
        vbox:
            xalign 0.5 yalign 0.9
            spacing 15
            text "Lab Assistant: [pcr_error]"
            text "In forensic analysis, precision is critical. Any deviation from"
            text "the proper protocol could compromise the evidence in court."
            text "We need to start over with a fresh sample."
            
            hbox:
                xalign 0.5
                spacing 20
                textbutton "Start Over":
                    style "back_button"
                    action [SetVariable("pcr_step", 0), SetVariable("pcr_state", "empty"),
                            SetVariable("pcr_error", "")]
                textbutton "Return to Lab":
                    style "back_button"
                    action [SetVariable("pcr_step", 0), SetVariable("pcr_state", "empty"),
                            SetVariable("pcr_error", ""), Jump('analytical_instruments')]


transform pcr_display_transform:
    zoom 0.35
    xpos 0.32
    ypos 0.2