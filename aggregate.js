[
  {
    $lookup:
      /**
       * from: The target collection.
       * localField: The local join field.
       * foreignField: The target join field.
       * as: The name for the results.
       * pipeline: Optional pipeline to run on the foreign collection.
       * let: Optional variables to use in the pipeline field stages.
       */
      {
        from: "Lv2",
        localField: "lv_2",
        foreignField: "_id",
        as: "lv_2",
      },
  },
  {
    $addFields:
      /**
       * newField: The new field name.
       * expression: The new field expression.
       */
      {
        lv_2: {
          $arrayElemAt: ["$lv_2", 0],
        },
      },
  },
  {
    $lookup:
      /**
       * from: The target collection.
       * localField: The local join field.
       * foreignField: The target join field.
       * as: The name for the results.
       * pipeline: Optional pipeline to run on the foreign collection.
       * let: Optional variables to use in the pipeline field stages.
       */
      {
        from: "Lv3",
        localField: "lv_2.lv_3",
        foreignField: "_id",
        as: "lv_2.lv_3",
      },
  },
  {
    $addFields:
      /**
       * newField: The new field name.
       * expression: The new field expression.
       */
      {
        "lv_2.lv_3": {
          $arrayElemAt: ["$lv_2.lv_3", 0],
        },
      },
  },
  {
    $lookup:
      /**
       * from: The target collection.
       * localField: The local join field.
       * foreignField: The target join field.
       * as: The name for the results.
       * pipeline: Optional pipeline to run on the foreign collection.
       * let: Optional variables to use in the pipeline field stages.
       */
      {
        from: "Lv4",
        localField: "lv_2.lv_3.lv_4",
        foreignField: "_id",
        as: "lv_2.lv_3.lv_4",
      },
  },
  {
    $lookup:
      /**
       * from: The target collection.
       * localField: The local join field.
       * foreignField: The target join field.
       * as: The name for the results.
       * pipeline: Optional pipeline to run on the foreign collection.
       * let: Optional variables to use in the pipeline field stages.
       */
      {
        from: "Lv5",
        localField: "lv_2.lv_3.lv_4.lv_5",
        foreignField: "_id",
        as: "_temp",
      },
  },
  {
    $addFields:
      /**
       * newField: The new field name.
       * expression: The new field expression.
       */
      {
        "lv_2.lv_3.lv_4": {
          $map: {
            input: "$lv_2.lv_3.lv_4",
            as: "ele",
            in: {
              $mergeObjects: [
                "$$ele",
                {
                  lv_5: {
                    $arrayElemAt: [
                      "$_temp",
                      {
                        $indexOfArray: ["$_temp._id", "$$ele.lv_5"],
                      },
                    ],
                  },
                },
              ],
            },
          },
        },
      },
  },
  {
    $lookup:
      /**
       * from: The target collection.
       * localField: The local join field.
       * foreignField: The target join field.
       * as: The name for the results.
       * pipeline: Optional pipeline to run on the foreign collection.
       * let: Optional variables to use in the pipeline field stages.
       */
      {
        from: "Lv6",
        localField: "lv_2.lv_3.lv_4.lv_5.lv_6",
        foreignField: "_id",
        as: "_temp",
      },
  },
];
