aggregate = [
    {
        '$lookup': {
            'from': 'Lv2',
            'localField': 'lv_2',
            'foreignField': '_id',
            'as': '_lv_2'
        }
    }, {
        '$lookup': {
            'from': 'Lv3',
            'localField': '_lv_2.lv_3',
            'foreignField': '_id',
            'as': '_lv_3'
        }
    }, {
        '$lookup': {
            'from': 'Lv4',
            'localField': '_lv_3.lv_4',
            'foreignField': '_id',
            'as': '_lv_4'
        }
    }, {
        '$lookup': {
            'from': 'Lv5',
            'localField': '_lv_4.lv_5',
            'foreignField': '_id',
            'as': '_lv_5'
        }
    }, {
        '$lookup': {
            'from': 'Lv6',
            'localField': '_lv_5.lv_6',
            'foreignField': '_id',
            'as': '_lv_6'
        }
    }, {
        '$lookup': {
            'from': 'Lv7',
            'localField': '_lv_6.lv_7',
            'foreignField': '_id',
            'as': '_lv_7'
        }
    }, {
        '$lookup': {
            'from': 'Lv8',
            'localField': '_lv_7.lv_8',
            'foreignField': '_id',
            'as': '_lv_8'
        }
    }, {
        '$addFields': {
            '_lv_7': {
                '$map': {
                    'input': '$_lv_7',
                    'as': 'ele',
                    'in': {
                        '$mergeObjects': [
                            '$$ele', {
                                'lv_8': {
                                    '$arrayElemAt': [
                                        '$_lv_8', {
                                            '$indexOfArray': [
                                                '$_lv_8._id', '$$ele.lv_8'
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            '_lv_6': {
                '$map': {
                    'input': '$_lv_6',
                    'as': 'ele',
                    'in': {
                        '$mergeObjects': [
                            '$$ele', {
                                'lv_7': {
                                    '$filter': {
                                        'input': '$_lv_7',
                                        'as': 'proc',
                                        'cond': {
                                            '$in': [
                                                '$$proc._id', '$$ele.lv_7'
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            '_lv_5': {
                '$map': {
                    'input': '$_lv_5',
                    'as': 'ele',
                    'in': {
                        '$mergeObjects': [
                            '$$ele', {
                                'lv_6': {
                                    '$arrayElemAt': [
                                        '$_lv_6', {
                                            '$indexOfArray': [
                                                '$_lv_6._id', '$$ele.lv_6'
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            '_lv_4': {
                '$map': {
                    'input': '$_lv_4',
                    'as': 'ele',
                    'in': {
                        '$mergeObjects': [
                            '$$ele', {
                                'lv_5': {
                                    '$arrayElemAt': [
                                        '$_lv_5', {
                                            '$indexOfArray': [
                                                '$_lv_5._id', '$$ele.lv_5'
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            '_lv_3': {
                '$map': {
                    'input': '$_lv_3',
                    'as': 'ele',
                    'in': {
                        '$mergeObjects': [
                            '$$ele', {
                                'lv_4': {
                                    '$filter': {
                                        'input': '$_lv_4',
                                        'as': 'proc',
                                        'cond': {
                                            '$in': [
                                                '$$proc._id', '$$ele.lv_4'
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            '_lv_2': {
                '$map': {
                    'input': '$_lv_2',
                    'as': 'ele',
                    'in': {
                        '$mergeObjects': [
                            '$$ele', {
                                'lv_3': {
                                    '$arrayElemAt': [
                                        '$_lv_3', {
                                            '$indexOfArray': [
                                                '$_lv_3._id', '$$ele.lv_3'
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            'lv_2': {
                '$arrayElemAt': [
                    '$_lv_2', 0
                ]
            }
        }
    }
]
