import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from projectQ.packages.values import RESULT_IMAGE_DIR, STATIC_DIR


NOT_TO_VISUALIZE = [
    'Yt', 'z1', 'z2', 'z3', 'z4', 'L_ArH', 'L_HH', 'Na_in', 'Na_out', 'K_out', 'K_in', 'Cl_out',
    'H_in', 'H_out', 'ATP', 'Hog1PPc', 'Hog1c', 'Hog1n', 'Pbs2', 'Pbs2PP', 'R_ref', 'r_os',
    'r_b', 'c_i', 'Sorbitol_out'
]

class Visualizer:
    def __init__(self):
        pass

    def plotTimeSeries(
        simulationData,
        SEQ,
        timeSeriesData=pd.DataFrame(),
        subplotLogic={},
        terms=False
    ):
        """ def description

        this function only needs the ODE results and the ORRESU_dict to
        visualise the time-series

        subplotLogic = {ylabel_str : correspondingSubstance_list}
        """

        if len(subplotLogic.keys()) == 0:
            subplotLogic[1] = 'a'
            generalizePlot = True
        else:
            generalizePlot = False

        sns.set_style(style='whitegrid')
        # context : dict, None, or one of {paper, notebook, talk, poster}
        sns.set_context(context='talk')
        fig = plt.figure(figsize=(10, 7.5))

        """fontSize 16 is a good size for the thesis"""
        fontSize = 16

        """create the subplots"""
        iterNum = 1

        """pre define the subplots structures"""
        for ORRESU, j in subplotLogic.items():
            exec('ax{0} = fig.add_subplot({1}, 1, {0})'.format(iterNum,
                                                                len(subplotLogic)))
            exec('ax{}.spines["top"].set_visible(False)'.format(iterNum))
            exec(
                'ax{}.spines["right"].set_visible(False)'.format(iterNum))
            exec(
                'ax{}.set_xlabel("time [s]",fontsize=fontSize)'.format(iterNum))

            """fix the y-axis lim for pictures for latex / publication"""
            # exec('ax{}.set_ylim(bottom=-20000, top=50000)'.format(iterNum))

            if generalizePlot == True:
                exec("ax{}.set_ylabel('no unit',fontsize=fontSize)".format(iterNum))
            else:
                exec('ax{}.set_ylabel(ORRESU,fontsize=fontSize)'.format(iterNum))

            iterNum += 1

        """x axis is shared and the ticks are rotated"""
        fig.autofmt_xdate(bottom=0.2,
                            rotation=30)
        fig.suptitle(t='{}_Model'.format(simulationData['type'].title()),
                        fontsize=fontSize)

        # fig.suptitle(t='Volume',
        #             fontsize=fontSize)

        with sns.color_palette('cubehelix', len(timeSeriesData.columns.tolist())):

            """make the fig more fittet"""
            # fig.tight_layout(pad = 3,
            #                 rect = [0,0,0.85,1]
            #                 )

            # """show the version of the plot"""
            # fig.text(0.99, 0.01,
            #          s='{} - {}'.format(current_date,
            #                             sql_USUBJID.title()),
            #          fontstyle='italic',
            #          color='#999999',
            #          ha='right',
            #          va='bottom',
            #          fontsize='x-small'
            #         )

            """assign each TESTCD to their right subplot"""
            if generalizePlot == False:
                for ORRESU_tuple, axis_index in zip(subplotLogic.items(),
                                                    range(1, len(subplotLogic)+1)):
                    parameter, substance = ORRESU_tuple

                    for i in substance:

                        if simulationData['type'] == 'combined_models' and i == 'Hog1PPn':
                            exec(
                                "ax{}.plot(timeSeriesData[i],label='Hog1PPn (*1E7)')".format(axis_index))

                        else:
                            if terms == True:
                                exec("ax{0}.plot(timeSeriesData[i],label=EquationTerms_dict[i])".format(
                                    axis_index))

                            else:
                                exec('ax{0}.plot(timeSeriesData[i],label=i)'.format(
                                    axis_index))

                        exec('ax{0}.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
                            frameon = True,loc={1!r},fontsize=fontSize)'.format(axis_index, 'center left'))

            else:
                plotLabels = timeSeriesData.columns.tolist()
                for i in plotLabels:
                    exec('ax1.plot(timeSeriesData[i],label=i)')
                    exec("ax1.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
                                frameon = True,loc='center left',fontsize=fontSize)")

            """"save the plot"""
            if not os.path.isdir(STATIC_DIR):
                os.mkdir(STATIC_DIR)
            if not os.path.isdir(RESULT_IMAGE_DIR):
                os.mkdir(RESULT_IMAGE_DIR)

            pictureName = '{0}_{1}.png'.format(simulationData['type'], SEQ)
            plt.savefig(
                RESULT_IMAGE_DIR + '/' + pictureName,
                dpi=360,
                format='png',
                bbox_inches='tight'
            )

            # """pre check if picture is already saved in database"""
            # cur.execute(sql.SQL("""
            #         Select max(seq) from {0}.analysis
            #         """).format(sql.Identifier(model.getName())))

            # if cur.fetchone()[0] != SEQ:
            #     cur.execute(sql.SQL("""
            #             INSERT INTO {0}.analysis(
            #                 seq, namepicture)
            #                 VALUES(%s, %s);
            #             """).format(sql.Identifier(model.getName())), [SEQ, pictureName])

            #     conn.commit()

            return pictureName

    def prepareVisualization(
        sql_USUBJID='',
        ODE_RESULTS=pd.DataFrame(),
        PDORRESU_x={}
    ):
        """conversion r to V

        convert the radius to the volume unit for better understandung of the
        cell system
        """

        # TEMP: temporary solution; PDORRESU = PDORRESU_x because otherwise it
        # overwrites the simulationSettingsForTimeRange['units'] dict --> local/global variable problem?
        if sql_USUBJID == 'combined_models':
            columnsOfDataframe = ODE_RESULTS.columns.tolist()

            ColumnsToVisualize = list(
                set(columnsOfDataframe) - set(NOT_TO_VISUALIZE))

            for i in NOT_TO_VISUALIZE:
                ODE_RESULTS = ODE_RESULTS.drop(columns=[i])

            PDORRESU = {
                i: PDORRESU_x[i] for i in ColumnsToVisualize if i in PDORRESU_x}

            try:
                ODE_RESULTS['Hog1PPn'] = ODE_RESULTS['Hog1PPn'] * 1E7
                # ODE_RESULTS['Cl_in'] = ODE_RESULTS['Cl_in'] / 10
            except:
                pass
        else:
            PDORRESU = PDORRESU_x

        convert_r_to_V = ['r', 'r_os', 'r_b', 'R_ref']
        ODE_RESULTS_columns = ODE_RESULTS.columns.tolist()
        for column_name in ODE_RESULTS_columns:

            if column_name in convert_r_to_V:
                ODE_RESULTS[column_name] = (
                    4/3) * np.pi * ODE_RESULTS[column_name]**3

                """"rename the column name

                change the first letter to 'V' and append then the rest of the
                old word string to this
                """
                new_column_name = 'V' + column_name[1:]
                ODE_RESULTS.rename(columns={column_name: new_column_name},
                                   inplace=True
                                   )
                """adapt the PDORRESU dict to the new units"""
                if column_name in PDORRESU:
                    PDORRESU[new_column_name] = PDORRESU.pop(column_name)
                    PDORRESU[new_column_name] = 'fL'

        """group the keys by their units"""
        groupedPDORRESU = {}
        for key, value in sorted(PDORRESU.items()):
            groupedPDORRESU.setdefault(value, []).append(key)

        """some design condition for the bachelor plots"""
        if sql_USUBJID == 'volume':
            ODE_RESULTS = pd.DataFrame(ODE_RESULTS['V'])
            groupedPDORRESU = {'total volume [fL]': ['V']}

        return ODE_RESULTS, groupedPDORRESU

